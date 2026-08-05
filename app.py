import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Socrates: Pedagogical Orchestrator", layout="wide")

# --- API KEY SETUP ---
# It will look for 'GOOGLE_API_KEY' in your Streamlit Secrets first.
# If not found, you can enter it in the sidebar.
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("🔑 Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.info("👋 Please enter your Gemini API Key in the sidebar or add it to Secrets to start.")

# --- HELPER FUNCTION: GEMINI PDF ENGINE ---
def process_pdf_with_gemini(uploaded_file, user_prompt):
    """Uploads file to Gemini, generates response, and cleans up."""
    with st.spinner("Socrates is reading the document..."):
        # 1. Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        
        try:
            # 2. Upload to Google Cloud (Native Gemini Support)
            pdf_file = genai.upload_file(path=tmp_path, display_name="textbook")
            
            # 3. Wait for Google to process the file
            while pdf_file.state.name == "PROCESSING":
                time.sleep(2)
                pdf_file = genai.get_file(pdf_file.name)
            
            # 4. Generate Content
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([pdf_file, user_prompt])
            
            # 5. Cleanup
            genai.delete_file(pdf_file.name)
            os.remove(tmp_path)
            
            return response.text
        except Exception as e:
            return f"Error: {e}"

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

# --- MAIN CONTENT ---
st.title("Socrates: Agentic Pedagogical Knowledge Orchestrator")
st.markdown("---")

if module == "Tutor (Persona-Adaptive)":
    st.header("Tutor: High-Context PDF Synthesis")
    uploaded_file = st.file_uploader("Ingest Technical PDF", type="pdf")
    tone = st.selectbox("Select Syntactic Persona", [
        "Senior Researcher", "Ivy League PhD Student", "Munna Bhai Lingo",
        "GATE Coaching Instructor", "UGCNET Coach", "Indian University Professor", "ENOUGH-TO-PASS-SEMESTER"
    ])
    question = st.text_input("Ask Socrates a question about this PDF:", "Summarize the core arguments of this text.")
    
    if uploaded_file and st.button("Synthesize"):
        prompt = f"Act as a {tone}. Based on the provided document, answer this: {question}"
        result = process_pdf_with_gemini(uploaded_file, prompt)
        st.markdown("### 🎓 Knowledge Synthesis")
        st.write(result)

elif module == "Research Gap Identifier":
    st.header("Research Gap Identifier")
    domain = st.selectbox("Select Domain", ["EEE", "AI/ML", "CSE", "Physics MSc"])
    user_query = st.text_area("Specific topic to analyze:")
    if st.button("Analyze Gap"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Analyze research gaps for {domain}: {user_query}. Provide 3 specific research directions.")
        st.write(response.text)

elif module == "Pedagogical Roadmap":
    st.header("Pedagogical Roadmap: Ontological Mapping")
    kg_data = {
        "Mathematics as Foundation": "Linear Algebra → underpins → Deep Learning; Calculus → drives → Optimization.",
        "Engineering Convergence": "Control Theory → Reinforcement Learning; Signal Processing → Computer Vision."
    }
    selected_kg = st.selectbox("Select Knowledge Graph", list(kg_data.keys()))
    st.info(kg_data[selected_kg])

elif module == "Philosophy and Epistemology":
    st.header("Philosophy and Epistemology")
    with st.expander("Philosophy of STEM"):
        st.write("**Philosophy of CS:** Ontological status of algorithms.")
        st.write("**Philosophy of AI:** Syntactic processing vs. semantic understanding.")
    with st.expander("Ancient Indian Philosophy"):
        st.write("**Nyāya-Vaiśeṣika:** Uses 5-step syllogism for formal AI inference.")

elif module == "CogniBridge (Vernacular: Banglish)":
    st.header("CogniBridge (Vernacular: Banglish)")
    uploaded_file = st.file_uploader("Upload Technical PDF for Banglish Translation", type="pdf")
    concept = st.text_input("Concept to explain (e.g. Normalization)", "Explain the main topic of the book")
    
    if uploaded_file and st.button("Distill to Banglish"):
        prompt = f"Explain the concept of {concept} from the document using 'Banglish' (Bengali + English mix). Make it very simple and easy to understand for a student."
        result = process_pdf_with_gemini(uploaded_file, prompt)
        st.markdown("### 🇧🇩 Banglish Synthesis")
        st.write(result)

# Fallback for other modules
else:
    st.info(f"The {module} module is currently in static/demo mode.")
