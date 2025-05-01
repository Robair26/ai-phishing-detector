import streamlit as st
import os
import requests
from detector import (
    is_phishing,
    extract_text_from_file,
    translate_to_english,
    log_detection_result,
    extract_urls,
    ml_detect
)
from datetime import datetime
import joblib

# Set up the page
st.set_page_config(page_title="AI Phishing Detector", layout="centered")
st.title("🛡️ AI-Powered Phishing Email Detector")

st.markdown("""
Upload an email file or paste the email content below. This tool will analyze the message for phishing keywords,
psychological manipulation, suspicious links, and provide ML-based prediction confidence.
""")

# Google Drive model URL
model_url = 'https://drive.google.com/uc?export=download&id=16Cffka8o8-JprSNX4vf40d5u9IXAtIpQ'
model_path = 'ml_model/phishing_model.pkl'

# Function to download the model from Google Drive
def download_model():
    st.info("Downloading the model... this may take a few moments.")
    r = requests.get(model_url, stream=True)
    with open(model_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    st.success("Model downloaded successfully!")

# Download the model if not already present
if not os.path.exists(model_path):
    download_model()

# Load the ML model
try:
    model = joblib.load(model_path)
    st.success("Model successfully loaded.")
except Exception as e:
    st.error(f"Failed to load the model: {e}")

# Main UI
verbose = st.checkbox("🔍 Verbose Output (Logs)")

uploaded_file = st.file_uploader("📁 Upload Email File (.txt, .pdf, .eml, .msg)", type=["txt", "pdf", "eml", "msg"])
manual_input = st.text_area("✍️ Or Paste Email Content", height=200)

if st.button("🚀 Analyze Email"):
    if uploaded_file:
        temp_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        content = extract_text_from_file(temp_path)
        os.remove(temp_path)
    elif manual_input.strip():
        content = manual_input
    else:
        st.warning("Please upload a file or paste email content.")
        st.stop()

    if verbose:
        st.info("📜 Original Text:\n" + content)

    translated = translate_to_english(content)
    if verbose and translated != content:
        st.info("🌍 Translated to English:\n" + translated)

    detected, score, confidence, reasons = is_phishing(translated)
    st.markdown(f"**🧠 Rule-Based Confidence:** {confidence}%")

    ml_result, ml_conf = ml_detect(translated)
    st.markdown(f"**🤖 ML Prediction:** {'PHISHING' if ml_result else 'SAFE'}")
    st.markdown(f"**🤖 ML Confidence:** {ml_conf}%")

    if verbose:
        st.write("🧠 Rule-Based Reasoning:")
        for reason in reasons:
            st.markdown(f"- {reason}")

    urls = extract_urls(translated)
    if urls:
        st.write("🔗 URLs Found:")
        for url in urls:
            st.write("-", url)
        if verbose:
            st.info(f"Scanned {len(urls)} URL(s).")

    if detected or ml_result:
        st.error(f"⚠️ This email is likely a PHISHING attempt. Rule Score: {score}/10")
    else:
        st.success("✅ This email appears safe.")

    log_detection_result(translated, detected)

    # -------------------- Phase 1: Feedback Button --------------------
    st.markdown("### 🤔 Was this detection accurate?")
    col1, col2 = st.columns(2)
    if not os.path.exists("feedback_log.txt"):
        open("feedback_log.txt", "w").close()

    with col1:
        if st.button("👍 Yes, this was correct"):
            with open("feedback_log.txt", "a", encoding="utf-8") as fb:
                fb.write(f"[{datetime.now()}] ✅ Correct — {'PHISHING' if detected or ml_result else 'SAFE'}\n")
                fb.write(f"{translated}\n{'-'*60}\n")
            st.success("Thanks for your feedback!")

    with col2:
        if st.button("👎 No, this was wrong"):
            with open("feedback_log.txt", "a", encoding="utf-8") as fb:
                fb.write(f"[{datetime.now()}] ❌ Wrong — {'PHISHING' if detected or ml_result else 'SAFE'}\n")
                fb.write(f"{translated}\n{'-'*60}\n")
            st.warning("Feedback noted. We’ll use this to improve!")
