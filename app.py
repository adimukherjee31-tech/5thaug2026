import streamlit as st
import os
import tempfile

# --- CRASH PREVENTION ---
try:
    import google.generativeai as genai
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except Exception as e:
    st.error("Library Load Error. Please check your requirements.txt")
    st.code(e)
    st.stop()

# --- APP SETUP ---
st.set_page_config(page_title="DBMS AI Tutor", layout="wide")
st.title("🎓 JNTUH DBMS AI Tutor")
st.caption("UGC NET & Exam Prep Mode Active")

with st.sidebar:
    st.header("1. Setup")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    uploaded_file = st.file_uploader("Upload DBMS PDF", type="pdf")
    
    st.header("2. Persona")
    tone = st.selectbox("Style", ["Professor", "Munnabhai (Hinglish)", "Simple"])
    
    if st.button("Clear Cache"):
        st.cache_resource.clear()
        st.success("Cache Cleared")

# --- MODEL FINDER ---
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if '1.5-flash' in m.name: return 'gemini-1.5-flash'
                if 'pro' in m.name: return 'gemini-pro'
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# --- CORE LOGIC ---
if api_key and uploaded_file:
    try:
        # Detect Model
        active_model = get_working_model(api_key)
        llm = ChatGoogleGenerativeAI(model=active_model, google_api_key=api_key)
        
        @st.cache_resource(show_spinner=False)
        def process_pdf(file):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            
            # Using PyPDFLoader - more stable for Streamlit
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_documents(pages[:200]) # Limit to 200 pages for speed
            
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_db = FAISS.from_documents(chunks, embeddings)
            return vector_db

        with st.spinner("Processing Textbook..."):
            db = process_pdf(uploaded_file)
        
        st.success(f"Tutor Ready! (Using {active_model})")

        # Chat
        query = st.chat_input("Ask a DBMS question...")
        if query:
            with st.chat_message("user"):
                st.write(query)
            
            docs = db.similarity_search(query, k=3)
            context = "\n\n".join([d.page_content for d in docs])
            
            styles = {
                "Professor": "Professional JNTUH Professor. Bullet points.",
                "Munnabhai (Hinglish)": "Munnabhai style. Hinglish, call them Mammu.",
                "Simple": "Explain like a child."
            }

            prompt = ChatPromptTemplate.from_template("""
            Context: {context}
            Persona: {style}
            Question: {question}
            Answer:""")
            
            chain = prompt | llm | StrOutputParser()
            
            with st.chat_message("assistant"):
                response = chain.invoke({"context": context, "style": styles[tone], "question": query})
                st.markdown(response)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👋 Enter your API Key and upload your PDF to begin.")
