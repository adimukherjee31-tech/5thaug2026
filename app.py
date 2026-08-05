import streamlit as st
import os

# --- CRITICAL: VERSION CHECK & ERROR CATCHING ---
try:
    import google.generativeai as genai
    import tempfile
    import time
except Exception as e:
    st.error(f"System boot error: {e}")
    st.stop()

# --- PAGE SETUP ---
st.set_page_config(page_title="Socrates AI", layout="wide")

# --- API KEY (SAFE LOADING) ---
# We check secrets safely to avoid the "Oh no" crash
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")

# --- NAVIGATION ---
st.sidebar.title("🏛️ Socrates Workbench")
module = st.sidebar.radio("Navigate Modules", [
    "Tutor (Persona-Adaptive)", 
    "Research Gap Identifier", 
    "Pedagogical Roadmap",
    "Philosophy and Epistemology",
    "Discovery Pathway",
    "CogniBridge (Banglish)"
])

st.title("Socrates: Pedagogical Knowledge Orchestrator")

# --- CORE FUNCTION: GEMINI PDF ENGINE ---
def process_pdf(uploaded_file, prompt_text):
    if not api_key:
        st.error("Missing API Key!")
        return
    
    with st.spinner("Socrates is analyzing the document..."):
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            
            # Upload using Gemini File API (No Langchain/FAISS needed)
            pdf_file = genai.upload_file(path=tmp_path, display_name="manual")
            
            # Wait for the file to be ready
            while pdf_file.state.name == "PROCESSING":
                time.sleep(2)
                pdf_file = genai.get_file(pdf_file.name)
            
            # Generate response
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([pdf_file, prompt_text])
            
            # Cleanup
            genai.delete_file(pdf_file.name)
            os.remove(tmp_path)
            return response.text
            
        except Exception as err:
            return f"AI Error: {err}"

# --- MODULES ---
if module == "Tutor (Persona-Adaptive)":
    st.header("Tutor: PDF Synthesis")
    uploaded_file = st.file_uploader("Upload PDF (DBMS / UGC NET)", type="pdf")
    tone = st.selectbox("Persona", ["Senior Researcher", "Munna Bhai", "UGCNET Coach", "Pass-Semester"])
    user_q = st.text_input("What should Socrates explain?", "Summarize the key points.")
    
    if uploaded_file and st.button("Synthesize"):
        ans = process_pdf(uploaded_file, f"Act as a {tone}. Explain: {user_q}")
        st.markdown(ans)

elif module == "CogniBridge (Banglish)":
    st.header("CogniBridge (Vernacular)")
    uploaded_file = st.file_uploader("Upload Technical PDF", type="pdf", key="bang")
    concept = st.text_input("Concept to explain in Banglish", "Relational Algebra")
    
    if uploaded_file and st.button("Distill"):
        ans = process_pdf(uploaded_file, f"Explain {concept} in Banglish (Bengali-English mix). Use funny local analogies.")
        st.markdown(ans)

elif module == "Research Gap Identifier":
    st.header("Research Gap Identifier")
    topic = st.text_input("Domain/Topic")
    if st.button("Identify Gaps") and api_key:
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(f"Suggest 3 research gaps for {topic}")
        st.write(res.text)

# Static Content for other modules
elif module == "Pedagogical Roadmap":
    st.header("Roadmap")
    st.write("Math → AI/ML → Engineering Interdependencies")

elif module == "Philosophy and Epistemology":
    st.header("Philosophy of STEM")
    st.write("Exploring the Socratic Method and Ancient logic in AI.")

elif module == "Discovery Pathway":
    st.header("Discovery Pathway")
    st.write("Inquiry-based learning paths.")

st.sidebar.markdown("---")
st.sidebar.caption("Stable Build: v2.1")
