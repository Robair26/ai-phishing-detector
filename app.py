import streamlit as st
import base64
import os
import fitz  # PyMuPDF
import email
import olefile
import extract_msg

# Theme selector
theme = st.selectbox("🌗 Select Theme", ["Light", "Dark"])

# Apply custom themes
def set_custom_theme(theme):
    if theme == "Dark":
        st.markdown(
            """
            <style>
                body {
                    background-color: #0e1117;
                    color: #ffffff;
                }
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
            """,
            unsafe_allow_html=True
        )

set_custom_theme(theme)

# Page title
st.markdown("## 🛡️ AI Phishing Detector")
st.markdown("Paste or upload email content to detect phishing threats.")

# File uploader
uploaded_file = st.file_uploader(
    "📎 Upload Email (.txt, .eml, .pdf, etc.):",
    type=["txt", "eml", "pdf"]
)

# Manual input area (label hidden, warning fixed)
manual_input = st.text_area("Manual Email Input", label_visibility="collapsed")

# Phishing keyword list
PHISHING_KEYWORDS = [
    "verify", "click here", "urgent", "password", "login", "account", "bank",
    "social security", "reset", "update", "confirm", "credentials", "alert",
    "security", "suspended"
]

def extract_text_from_pdf(file):
    text = ""
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def extract_text_from_eml(file):
    try:
        msg = email.message_from_bytes(file.read())
        if msg.is_multipart():
            return ''.join(part.get_payload(decode=True).decode(errors="ignore")
                           for part in msg.walk()
                           if part.get_content_type() == "text/plain")
        else:
            return msg.get_payload(decode=True).decode(errors="ignore")
    except Exception as e:
        st.error(f"Error reading EML: {e}")
        return ""

def detect_phishing(content):
    matches = [kw for kw in PHISHING_KEYWORDS if kw.lower() in content.lower()]
    if matches:
        st.error(f"⚠️ This email is likely a PHISHING attempt.\n\n**Matched keywords:** {', '.join(matches)}")
    else:
        st.success("✅ This email appears safe.")

# Analyze button
if st.button("🚀 Analyze"):
    text = ""

    if uploaded_file:
        ext = os.path.splitext(uploaded_file.name)[-1].lower()
        if ext == ".txt":
            text = uploaded_file.read().decode(errors="ignore")
        elif ext == ".eml":
            text = extract_text_from_eml(uploaded_file)
        elif ext == ".pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            st.error("Unsupported file format.")
    elif manual_input:
        text = manual_input

    if text:
        detect_phishing(text)
    else:
        st.warning("⚠️ Please provide email content to analyze.")
