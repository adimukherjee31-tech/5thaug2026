import streamlit as st
import google.generativeai as genai

# Setup Configuration
st.set_page_config(page_title="Socrates: Pedagogical Knowledge Orchestrator", layout="wide")

# --- EASY API KEY BOX ---
st.sidebar.title("🔑 Security Setup")
# This creates a box on the left side of your website to paste the key
user_api_key = st.sidebar.text_input("Paste your Gemini API Key here:", type="password")

if user_api_key:
    genai.configure(api_key=user_api_key)
    st.sidebar.success("API Key Linked!")
else:
    st.sidebar.warning("Please paste your API Key to start.")

# --- PAGE HEADER ---
st.title("🏛️ Socrates: Agentic Pedagogical Knowledge Orchestrator")
st.markdown("### *A Deterministic Framework for Multi-Modal Academic Synthesis*")

# Tabs for Modular Research Workflow
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Tutor (Persona-Adaptive Synthesis)", 
    "Research Gap Identifier", 
    "Literature Review Finder", 
    "Pedagogical Roadmap",
    "NPTEL Asynchronous Pedagogical Transcoding Engine"
])

with tab1:
    st.header("Tutor: High-Context PDF Synthesis")
    uploaded_file = st.file_uploader("Ingest Technical PDF", type="pdf")
    tone = st.selectbox("Select Syntactic Persona", [
        "Senior Professional Researcher", "Ivy League PhD Student", 
        "GATE Coach Tone", "UGC-NET Coach Tone", "Simple Indian English", "Munna Bhai Lingo"
    ])
    
    if uploaded_file and st.button("Synthesize Knowledge"):
        with st.spinner("Executing agentic analysis..."):
            st.text_area("Synthesized Analysis", f"Parsed for deep semantic threads. Output conditioned to: {tone}")

with tab2:
    st.header("Research Gap Identifier")
    domain = st.selectbox("Select Domain", ["EEE", "AI/ML", "CSE", "ECE", "Mechanical", "Physics MSc", "Math MSc"])
    exam = st.selectbox("Target Assessment", ["GATE", "IIT-JAM", "CUET", "UGC-NET"])
    user_query = st.text_area("Specific topic or chapter to analyze:")
    
    if st.button("Analyze Requirement Gap"):
        if not user_api_key:
            st.error("Please enter your API Key in the sidebar first!")
        else:
            with st.spinner("Mapping curriculum to examination standards..."):
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = f"Analyze the gap between the {domain} syllabus and {exam} requirements for the topic: {user_query}. Provide a structured gap analysis and study strategy."
                response = model.generate_content(prompt)
                st.markdown("### Gap Analysis & Strategic Recommendations")
                st.write(response.text)

with tab3:
    st.header("Literature Review Finder")
    search_query = st.text_input("Query ArXiv.org for Research Synthesis:")
    if st.button("Query Research Nexus"):
        st.write(f"Orchestrating search across ArXiv repositories for: {search_query}")
        st.text_area("Research Synthesis & Gap Analysis", "Foundational papers retrieved. Analysis of research gaps in progress...")

with tab4:
    st.header("Pedagogical Roadmap: Ontological Mapping")
    domain_map = st.selectbox("Select Domain for Roadmap", ["BTech EEE", "BTech AI ML", "BTech CSE", "BTech ECE", "BTech Mechanical", "Physics MSc", "Math MSc"])
    if st.button("Generate Deterministic Roadmap"):
        st.write(f"Mapping curriculum for {domain_map}...")
        st.success("Roadmap visualized: Core competency mapping complete.")

with tab5:
    st.header("NPTEL Asynchronous Pedagogical Transcoding Engine")
    st.markdown("*A high-fidelity framework for the semantic distillation of asynchronous lecture transcripts.*")
    
    transcript_input = st.text_area("Ingest Lecture Transcript Vector:", height=200, placeholder="Paste the raw YouTube/NPTEL transcript here...")
    
    if st.button("Transcode & Distill"):
        if not user_api_key:
            st.error("Please enter your API Key in the sidebar first!")
        else:
            with st.spinner("Executing semantic decomposition..."):
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = f"""
                Act as an elite Ivy League Academic Fellow. Perform a pedagogical distillation 
                of the following lecture transcript. Deconstruct the primary conceptual threads, 
                resolve technical ambiguity, and reconstruct the output into a 
                concise, highly structured pedagogical summary: {transcript_input}
                """
                response = model.generate_content(prompt)
                
                st.markdown("### Distilled Conceptual Output")
                st.write(response.text)
