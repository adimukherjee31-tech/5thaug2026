import streamlit as st
import os
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- PAGE CONFIG ---
st.set_page_config(page_title="DBMS AI Tutor", layout="wide")
st.title("🎓 JNTUH DBMS AI Tutor")
st.caption("Lightweight Version: Fast & Stable for Exam Prep")

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. Setup")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    st.header("2. Study Mode")
    tone = st.selectbox("Teaching Style", ["Professor", "Munnabhai (Hinglish)", "Simple"])

# --- CORE LOGIC ---
if api_key and uploaded_file:
    try:
        # Initialize Gemini components using the same API Key
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # Lightweight Embeddings from Google
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Stable Chat Model
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        
        @st.cache_resource(show_spinner=False)
        def process_pdf(file):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()
            
            # Splitting text
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_documents(pages[:200]) # Read first 200 pages
            
            # Creating Knowledge Base
            vector_db = FAISS.from_documents(chunks, embeddings)
            return vector_db

        with st.spinner("Analyzing Textbook..."):
            db = process_pdf(uploaded_file)
        
        st.success("Ready! Ask me anything.")

        # --- CHAT ---
        query = st.chat_input("Ask a question (e.g. explain ACID properties)")
        if query:
            with st.chat_message("user"):
                st.write(query)
            
            # Retrieval
            docs = db.similarity_search(query, k=3)
            context = "\n\n".join([d.page_content for d in docs])
            
            styles = {
                "Professor": "Professional JNTUH Professor. Use bullet points.",
                "Munnabhai (Hinglish)": "Munnabhai style. Use Hinglish, call the student Mammu.",
                "Simple": "Explain like a 10-year-old."
            }

            prompt = ChatPromptTemplate.from_template("""
            Context: {context}
            Style: {style}
            Question: {question}
            
            Answer:""")
            
            chain = prompt | llm | StrOutputParser()
            
            with st.chat_message("assistant"):
                response = chain.invoke({
                    "context": context, 
                    "style": styles[tone], 
                    "question": query
                })
                st.markdown(response)

    except Exception as e:
        st.error(f"System Error: {e}")
        st.info("Check if your API Key is valid and has Gemini access.")
else:
    st.info("👋 Enter your API Key and upload your PDF to start.")
