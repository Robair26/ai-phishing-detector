import streamlit as st
from detector import (
    is_phishing,
    extract_text_from_file,
    extract_urls,
    translate_to_english
)
import os
import tempfile

# Title and layout
st.set_page_config(page_title="AI Phishing Detector", layout="centered")
st.title("🛡️ AI-Powered Phishing Email Detector")

# Theme toggle
theme = st.selectbox("🌗 Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
            body { background-color: #0e1117; color: white; }
            .stTextInput > div > div > input,
            .stTextArea > div > textarea {
                background-color: #262730;
                color: white;
            }
            .stButton > button {
                background-color: #ff4b4b;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# Text input
user_input = st.text_area("📩 Paste email content here", height=200)

# File upload
uploaded_file = st.file_uploader("📎 Or upload a .txt, .eml, .msg, or .pdf file", type=["txt", "eml", "msg", "pdf"])

email_content = ""

if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    email_content = extract_text_from_file(tmp_path)
    os.remove(tmp_path)

elif user_input:
    email_content = user_input

if st.button("🚨 Analyze Email"):
    if email_content.strip():
        st.info("🔍 Analyzing email content...")
        
        # Detect language and translate
        translated_content = translate_to_english(email_content)
        
        # Display URLs
        urls = extract_urls(translated_content)
        if urls:
            st.markdown("🔗 **Links found in email:**")
            for url in urls:
                st.markdown(f"- {url}")
        else:
            st.markdown("✅ No links found in the email.")

        # Detect phishing
        if is_phishing(translated_content):
            st.error("⚠️ This email is likely a **PHISHING attempt**.")
        else:
            st.success("✅ This email appears **safe**.")
    else:
        st.warning("⚠️ Please paste content or upload a file.")
