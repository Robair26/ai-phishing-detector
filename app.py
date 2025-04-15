import streamlit as st
from detector import (
    is_phishing,
    extract_text_from_file,
    translate_to_english,
    extract_urls,
    check_links,
    log_detection_result
)
import os

st.set_page_config(page_title="AI Phishing Detector", layout="centered")
st.title("🛡️ AI-Powered Phishing Email Detector")

st.markdown("""
Upload an email file or paste the email content below. This tool will analyze the message for phishing keywords,
psychological manipulation, and suspicious links.
""")

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

    detected, score = is_phishing(translated)

    urls = extract_urls(translated)
    if urls:
        st.write("🔗 URLs Found:")
        for url in urls:
            st.write("-", url)
        if verbose:
            st.info(f"Scanned {len(urls)} URL(s).")

    if detected:
        st.error(f"⚠️ This email is likely a PHISHING attempt. Threat Score: {score}/10")
    else:
        st.success("✅ This email appears safe.")

    log_detection_result(translated, detected)
