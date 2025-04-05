import streamlit as st
import fitz  # PyMuPDF
import extract_msg
import chardet
from detector import predict_phishing
import base64

# Theme selector
theme = st.selectbox("🌗 Select Theme", ["Light", "Dark"])

# Apply custom theme
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
    else:
        st.markdown(
            """
            <style>
                body {
                    background-color: #ffffff;
                    color: #000000;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

set_custom_theme(theme)

# App Header
st.markdown("<h1 style='text-align: center;'>🛡️ AI Phishing Detector</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Paste or upload email content to detect phishing threats.</p>", unsafe_allow_html=True)
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("📎 Upload Email (.txt, .eml, .pdf):", type=["txt", "eml", "pdf"])

# Text input
email_input = st.text_area("Or paste the email subject or message here:")

# File processing
def extract_text(file):
    if file.name.endswith(".txt"):
        bytes_data = file.read()
        encoding = chardet.detect(bytes_data)["encoding"]
        return bytes_data.decode(encoding)
    elif file.name.endswith(".eml"):
        msg = extract_msg.Message(file)
        return msg.body
    elif file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    return ""

if st.button("🚀 Analyze"):
    content = ""

    if uploaded_file:
        content = extract_text(uploaded_file)
    elif email_input:
        content = email_input

    if not content.strip():
        st.warning("⚠️ Please provide email content.")
    else:
        prediction, confidence = predict_phishing(content)

        if prediction == 1:
            st.error(f"🚨 This email is likely **PHISHING**. Confidence: {confidence:.2%}")
        else:
            st.success(f"✅ This email appears **SAFE**. Confidence: {confidence:.2%}")
