import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import io

# Setup Configuration
st.set_page_config(page_title="Socrates: Pedagogical Knowledge Orchestrator", layout="wide")

# --- API KEY HANDLING ---
# Priority: 1. Streamlit Secrets, 2. Manual Sidebar Input
api_key = st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter your Gemini API Key in the sidebar to enable AI features.")

# --- HELPER FUNCTION: PDF TEXT EXTRACTION ---
def get_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    # Limit to first 100 pages to avoid memory crashes on free servers
    for page in reader.pages[:100]:
        text += page.extract_text() + "\n"
    return text

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
    user_question = st.text_input("Ask a specific question about this PDF:")
    tone = st.selectbox("Select Syntactic Persona", [
        "Senior Researcher", "Ivy League PhD Student", "Munna Bhai Lingo",
        "GATE Coaching Instructor", "UGCNET Coach", "MIT STEM PROFESSOR INSIGHTS", 
        "INDIAN UNIVERSITY PROFESSOR DIALECT", "ENOUGH-TO-PASS-SEMESTER"
    ])
    
    if uploaded_file and st.button("Synthesize"):
        with st.spinner(f"Socrates is channeling {tone}..."):
            try:
                # 1. Extract text simply
                raw_text = get_pdf_text(uploaded_file)
                # 2. Call Gemini
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
                You are acting as: {tone}.
                Below is the content of a technical document. 
                Question: {user_question if user_question else 'Summarize the core ontological concepts of this text.'}
                
                Document Content:
                {raw_text[:30000]} # Sending first 30k chars to keep it fast
                """
                response = model.generate_content(prompt)
                st.markdown("### Synthesized Insight")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

elif module == "Research Gap Identifier":
    st.header("Research Gap Identifier")
    domain = st.selectbox("Select Domain", ["EEE", "AI/ML", "CSE", "Physics MSc"])
    user_query = st.text_area("Specific topic to analyze:")
    if st.button("Analyze Gap"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Analyze research gaps for {domain}: {user_query}. Provide 3 specific novel ideas.")
        st.write(response.text)

elif module == "NPTEL Transcoding Engine":
    st.header("NPTEL Asynchronous Pedagogical Transcoding Engine")
    transcript = st.text_area("Paste NPTEL/Lecture Transcript:", height=200)
    if st.button("Transcode & Distill"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Perform pedagogical distillation on this lecture transcript. Break it down into Core Principles and Exam-oriented notes: {transcript}")
        st.write(response.text)

elif module == "Philosophy and Epistemology":
    st.header("Philosophy and Epistemology")
    st.info("Explore the structural foundations of knowledge.")
    with st.expander("Philosophy of Disciplinary Fields"):
        st.write("**Philosophy of CS:** Ontological status of algorithms.")
        st.write("**Philosophy of EEE:** Teleology of control systems.")
    # (Keep your other expanders here as they are static and work fine)

elif module == "CogniBridge (Vernacular: Banglish)":
    st.header("CogniBridge (Vernacular: Banglish)")
    st.markdown("<sub>*Translates your dense, dry textbook to simple banglish*</sub>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload core academic PDF for ingestion", type="pdf", key="banglish_upload")
    concept_input = st.text_area("Concept to explain in Banglish (e.g. Relational Algebra):")
    
    if uploaded_file and st.button("Distill to Banglish"):
        with st.spinner("Translating to Banglish..."):
            try:
                raw_text = get_pdf_text(uploaded_file)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
                Explain the following concept in 'Banglish' (Bengali mixed with English). 
                Keep the tone extremely helpful like a friendly senior student helping a junior.
                Concept/Context from book: {raw_text[:20000]}
                Target Topic: {concept_input}
                """
                response = model.generate_content(prompt)
                st.markdown("### Banglish Synthesis")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# (Default Discovery Pathway and Literature Review sections stay as your placeholders)
else:
    st.info("Module under orchestration. Please select a functional module from the sidebar.")
