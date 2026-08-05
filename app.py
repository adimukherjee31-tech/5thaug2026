import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# 1. SETUP & THEME
st.set_page_config(page_title="Socrates Workbench", layout="wide")

# 2. API KEY HANDLER
st.sidebar.title("🏛️ Socrates Setup")
api_key = st.sidebar.text_input("🔑 Paste Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("Please enter your API Key to enable the AI features.")

# 3. NAVIGATION
module = st.sidebar.radio("Navigate Modules", [
    "Tutor (Persona-Adaptive)", 
    "Research Gap Identifier", 
    "Pedagogical Roadmap",
    "Philosophy and Epistemology",
    "CogniBridge (Vernacular: Banglish)"
])

# 4. HELPER: PDF READER
def get_pdf_text(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content: text += content
        return text[:30000] # Safe limit for Gemini Flash
    except Exception as e:
        return f"Error: {e}"

# --- MAIN CONTENT ---
st.title("Socrates: Agentic Pedagogical Orchestrator")
st.markdown("---")

if module == "Tutor (Persona-Adaptive)":
    st.header("Tutor: High-Context PDF Synthesis")
    uploaded_file = st.file_uploader("Upload Technical PDF (DBMS/NET)", type="pdf")
    tone = st.selectbox("Select Persona", [
        "Senior Researcher", "Munna Bhai Lingo", "UGCNET Coach", "Indian University Professor", "ENOUGH-TO-PASS-SEMESTER"
    ])
    question = st.text_input("What should Socrates explain?", "Summarize the core concepts.")

    if uploaded_file and st.button("Synthesize") and api_key:
        with st.spinner("Socrates is analyzing..."):
            context = get_pdf_text(uploaded_file)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Act as a {tone}. Using this context: {context}, answer: {question}"
            response = model.generate_content(prompt)
            st.markdown(response.text)

elif module == "Research Gap Identifier":
    st.header("Research Gap Identifier")
    domain = st.selectbox("Select Domain", ["AI/ML", "CSE", "EEE", "Physics"])
    topic = st.text_area("Specific topic to analyze:")
    if st.button("Analyze Gap") and api_key:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Analyze research gaps for {domain}: {topic}. Suggest 3 PhD directions.")
        st.write(response.text)

elif module == "CogniBridge (Vernacular: Banglish)":
    st.header("CogniBridge (Banglish Mode)")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="bang")
    concept = st.text_input("Concept to explain in Banglish:")

    if uploaded_file and st.button("Distill to Banglish") and api_key:
        with st.spinner("Synthesizing..."):
            context = get_pdf_text(uploaded_file)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Explain '{concept}' in 'Banglish' (Bengali + English mix). Use funny local analogies. Context: {context}"
            response = model.generate_content(prompt)
            st.write(response.text)

elif module == "Pedagogical Roadmap":
    st.header("Pedagogical Roadmap: Ontological Mapping")
    st.info("Mathematics → AI/ML → Engineering Interdependencies")
    st.write("**Mathematics:** Linear Algebra & Calculus underpin Deep Learning.")
    st.write("**Engineering:** Signal Processing feeds into Computer Vision.")

elif module == "Philosophy and Epistemology":
    st.header("Philosophy of STEM")
    with st.expander("Ancient Indian Philosophy"):
        st.write("**Nyāya-Vaiśeṣika:** 5-step syllogism for formal AI inference.")
    with st.expander("Greek Traditions"):
        st.write("**Socratic Method:** Dialectical inquiry for logic debugging.")

st.sidebar.markdown("---")
if st.sidebar.button("Clear App Cache"):
    st.cache_resource.clear()
    st.rerun()
