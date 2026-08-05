import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- PAGE SETUP ---
st.set_page_config(page_title="Socrates Workbench", layout="wide")

# --- API KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("🔑 Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Enter API Key in Sidebar to start.")

# --- NAVIGATION ---
st.sidebar.title("🏛️ Socrates Workbench")
module = st.sidebar.radio("Navigate", [
    "Tutor (Persona-Adaptive)", 
    "Research Gap Identifier", 
    "Pedagogical Roadmap",
    "Philosophy & STEM",
    "CogniBridge (Banglish)"
])

st.title("Socrates: Agentic Pedagogical Orchestrator")

# --- HELPER: SIMPLE PDF READER ---
def get_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# --- MODULES ---
if module == "Tutor (Persona-Adaptive)":
    st.header("Tutor: PDF Synthesis")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    tone = st.selectbox("Select Persona", ["Senior Researcher", "Munna Bhai", "UGCNET Coach", "Professor"])
    query = st.text_input("What should Socrates explain?", "Summarize the key concepts.")

    if uploaded_file and st.button("Synthesize") and api_key:
        with st.spinner("Socrates is reading..."):
            text = get_pdf_text(uploaded_file)
            model = genai.GenerativeModel("gemini-1.5-flash")
            # We send only the first 30,000 characters to ensure it doesn't crash
            prompt = f"Act as a {tone}. Based on this text: {text[:30000]}, answer this: {query}"
            response = model.generate_content(prompt)
            st.markdown(response.text)

elif module == "Research Gap Identifier":
    st.header("Research Gap Identifier")
    topic = st.text_input("Research Topic / Domain")
    if st.button("Analyze") and api_key:
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(f"Suggest 3 novel research gaps for {topic} suitable for a PhD proposal.")
        st.write(res.text)

elif module == "CogniBridge (Banglish)":
    st.header("CogniBridge (Banglish Mode)")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="bang")
    concept = st.text_input("Concept to explain", "Relational Algebra")

    if uploaded_file and st.button("Explain") and api_key:
        with st.spinner("Processing..."):
            text = get_pdf_text(uploaded_file)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Explain the concept '{concept}' in Banglish (Bengali+English mix) using this context: {text[:20000]}"
            response = model.generate_content(prompt)
            st.write(response.text)

elif module == "Pedagogical Roadmap":
    st.header("Pedagogical Roadmap")
    st.info("Mathematics → AI/ML → Engineering Interdependencies")
    st.write("1. Linear Algebra (Foundation)\n2. Optimization (Mechanics)\n3. Neural Networks (Application)")

elif module == "Philosophy & STEM":
    st.header("Philosophy and Epistemology")
    st.write("**Nyāya-Vaiśeṣika:** Logic for AI.\n**Socratic Method:** Debugging logic.")

st.sidebar.markdown("---")
st.sidebar.caption("Socrates Stable Build v3.0")
