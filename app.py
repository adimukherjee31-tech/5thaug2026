import streamlit as st
import os
import tempfile
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- PAGE CONFIG ---
st.set_page_config(page_title="DBMS AI Tutor", layout="wide")
st.title("🎓 JNTUH DBMS AI Tutor")
st.markdown("---")

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get from Google AI Studio")
    uploaded_file = st.file_uploader("Upload DBMS Textbook (PDF)", type="pdf")
    
    st.header("⚙️ Settings")
    tone = st.selectbox("Teaching Style", ["Professor (Formal)", "Munnabhai (Hinglish)", "Class 8 (Simple)"])
    page_limit = st.slider("Pages to Index", 10, 500, 200)
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API Key Connected!")
        except:
            st.error("Invalid API Key")

# --- AUTO-MODEL DISCOVERY ---
def get_best_model(key):
    try:
        genai.configure(api_key=key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Clean naming for LangChain
        clean_names = [n.replace('models/', '') for n in available_models]
        for target in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
            if target in clean_names:
                return target
        return clean_names[0]
    except:
        return "gemini-1.5-flash"

# --- MAIN ENGINE ---
if api_key and uploaded_file:
    try:
        # 1. Initialize AI
        working_model = get_best_model(api_key)
        llm = ChatGoogleGenerativeAI(model=working_model, google_api_key=api_key)

        # 2. Process Document (Cached for speed)
        @st.cache_resource(show_spinner=False)
        def process_textbook(file, limit):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            
            loader = PyMuPDFLoader(tmp_path)
            docs = loader.load()[:limit]
            
            # Split text into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_documents(docs)
            
            # Create Vector Knowledge Base
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_db = FAISS.from_documents(chunks, embeddings)
            os.remove(tmp_path)
            return vector_db

        with st.spinner("📚 Reading textbook... Hang tight!"):
            db = process_textbook(uploaded_file, page_limit)
        
        st.sidebar.info(f"Active Model: {working_model}")

        # 3. Chat Interface
        query = st.chat_input("Ask a question from the book...")
        if query:
            with st.chat_message("user"):
                st.write(query)
            
            # Retrieval
            relevant_docs = db.similarity_search(query, k=4)
            context = "\n\n".join([d.page_content for d in relevant_docs])
            
            # Personalities
            styles = {
                "Professor (Formal)": "Professional JNTUH Professor. Bullet points, exam-focused.",
                "Munnabhai (Hinglish)": "Munnabhai style. Use Tapori Hinglish and call the student Mammu.",
                "Class 8 (Simple)": "Simple English. Use toy analogies."
            }
            
            # Prompting
            prompt = ChatPromptTemplate.from_template("""
            You are a subject matter expert in DBMS.
            
            Context from Textbook: {context}
            Style instructions: {style}
            User Question: {question}
            
            Answer strictly based on context if possible. If not, use general DBMS knowledge.
            """)
            
            # Execution
            chain = prompt | llm | StrOutputParser()
            
            with st.chat_message("assistant"):
                response = chain.invoke({
                    "context": context,
                    "style": styles[tone],
                    "question": query
                })
                st.markdown(response)

    except Exception as e:
        st.error(f"System encountered an error: {e}")
else:
    st.info("👋 Welcome! Please enter your API Key and upload a PDF in the sidebar to start.")
