import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# 1. SETUP PAGE
st.set_page_config(page_title="Socrates Workbench", layout="wide")

# 2. SIDEBAR - API KEY INPUT (Instead of Secrets)
st.sidebar.title("🏛️ Socrates Setup")
user_api_key = st.sidebar.text_input("Paste your Google API Key here:", type="password")

if user_api_key:
    genai.configure(api_key=user_api_key)
else:
    st.sidebar.warning("⚠️ Please paste your API Key to start.")

# 3. NAVIGATION
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

# 4. HELPER FUNCTION
def get_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text[:25000] # Limit text
