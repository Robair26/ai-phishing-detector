import streamlit as st
import logging
from detector import is_phishing, extract_text_from_file
from link_scanner import check_links
import os

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

st.set_page_config(page_title="AI Phishing Detector", layout="wide")

# Theme selector
theme = st.selectbox("🌗 Select Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
            body { background-color: #0e1117; color: white; }
            .stTextInput > div > div > input, .stTextArea > div > textarea {
                background-color: #262730; color: white;
            }
            .stButton > button { background-color: #ff4b4b; color: white; }
        </style>
        """, unsafe_allow_html=True
    )

# Title
st.title("🛡️ AI Phishing Detector (Multilingual)")

# File Upload
uploaded_file = st.file_uploader("📎 Upload Email (.txt, .eml, .msg, .pdf)", type=["txt", "eml", "msg", "pdf"])
email_text = ""

# OR Manual Input
with st.expander("✍️ Paste Email Text Manually"):
    email_text = st.text_area("Email Content", height=200)

# Combine inputs
if uploaded_file is not None:
    # Save temp file
    path = os.path.join("temp_input", uploaded_file.name)
    os.makedirs("temp_input", exist_ok=True)
    with open(path, "wb") as f:
        f.write(uploaded_file.read())
    email_text = extract_text_from_file(path)

if email_text:
    st.markdown("---")
    st.subheader("🔎 Results")

    with st.spinner("Analyzing..."):
        result = is_phishing(email_text)

        st.write("✅ Email content processed.")
        if result:
            st.error("⚠️ This email is likely a **PHISHING** attempt.")
        else:
            st.success("✅ This email appears **SAFE**.")

else:
    st.info("📬 Please upload a file or paste some email content.")
