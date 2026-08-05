import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Setup Configuration
st.set_page_config(page_title="Socrates: Pedagogical Knowledge Orchestrator", layout="wide")

# Ensure API Key is handled safely
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")

# --- HELPER: PDF READER ---
def get_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content: text += content
    return text[:30000] # Limit for stability

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏛️ Socrates Workbench")
module = st.sidebar.radio("Navigate Modules", [
    "Tutor (Persona-Adaptive)", 
    "Research Gap Identifier", 
    "Literature Review Finder", 
    "Pedagogical Roadmap",
    "NPTEL Transcoding Engine",
    "Philosophy and Epistemology",
    "Discovery Pathway",
    "CogniBridge (Vernacular: Banglish)"
])

# --- MAIN CONTENT AREA ---
st.title("Socrates: Agentic Pedagogical Knowledge Orchestrator")

if module == "Tutor (Persona-Adaptive)":
    st.header("Tutor: High-Context PDF Synthesis")
    uploaded_file = st.file_uploader("Ingest Technical PDF", type="pdf")
    tone = st.selectbox("Select Syntactic Persona", [
        "Senior Researcher", "Ivy League PhD Student", "Munna Bhai Lingo",
        "MIT STEM Professor Insights", "UGCNET Coach", "Indian University Professor", "ENOUGH-TO-PASS-SEMESTER"
    ])
    query = st.text_input("What should Socrates explain from this PDF?", "Summarize the key exam points.")
    
    if uploaded_file and st.button("Synthesize"):
        with st.spinner(f"Synthesizing as {tone}..."):
            context = get_pdf_text(uploaded_file)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Act as a {tone}. Based on this text: {context}, answer: {query}"
            response = model.generate_content(prompt)
            st.markdown(response.text)

elif module == "Research Gap Identifier":
    st.header("Research Gap Identifier")
    domain = st.selectbox("Select Domain", ["EEE", "AI/ML", "CSE", "Physics MSc"])
    user_query = st.text_area("Specific topic to analyze:")
    if st.button("Analyze Gap"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Analyze research gaps for {domain}: {user_query}. Suggest 3 PhD directions.")
        st.write(response.text)

elif module == "Pedagogical Roadmap":
    st.header("Pedagogical Roadmap: Ontological Mapping")
    kg_data = {
        "Mathematics as Foundation": "Linear Algebra → underpins → Deep Learning; Calculus → drives → Optimization.",
        "Engineering to AI/ML": "Control Theory → Reinforcement Learning; Signal Processing → Computer Vision."
    }
    selected_kg = st.selectbox("Select Knowledge Graph", list(kg_data.keys()))
    st.info(kg_data[selected_kg])

elif module == "NPTEL Transcoding Engine":
    st.header("NPTEL Asynchronous Transcoding")
    transcript = st.text_area("Paste NPTEL Transcript:", height=200)
    if st.button("Transcode & Distill"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Simplify this NPTEL lecture into 5 exam points: {transcript}")
        st.write(response.text)

elif module == "Philosophy and Epistemology":
    st.header("Philosophy and Epistemology")
    with st.expander("Philosophy of Disciplinary Fields"):
        st.write("**Philosophy of CS:** Algorithms as mathematical vs physical objects.")
    with st.expander("Ancient Indian Philosophy"):
        st.write("**Nyāya-Vaiśeṣika:** Formal 5-step syllogism for AI inference.")
    with st.expander("Greek Traditions"):
        st.write("**Socratic Method:** Dialectical inquiry for logic debugging.")

elif module == "CogniBridge (Vernacular: Banglish)":
    st.header("CogniBridge (Banglish Mode)")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="bang")
    concept = st.text_input("Concept to explain in Banglish:")
    if uploaded_file and st.button("Distill"):
        context = get_pdf_text(uploaded_file)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Explain '{concept}' in Banglish (Bengali+English mix) using local analogies. Context: {context}"
        response = model.generate_content(prompt)
        st.write(response.text)

st.sidebar.markdown("---")
st.sidebar.caption("Socrates v3.0 | Research & Exam Prep")
