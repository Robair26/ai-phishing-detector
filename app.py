import streamlit as st
from detector import (
    is_phishing,
    extract_text_from_file,
    translate_to_english,
    extract_urls,
    get_sentiment,
    detect_social_engineering,
    analyze_pos_patterns,
    check_links,
    log_detection_result,
    get_domain_reputation
)
import os

st.set_page_config(page_title="AI Phishing Detector", layout="centered")
st.title("🛡️ AI-Powered Phishing Email Detector")

st.markdown("""
Upload an email file or paste the email content below. This tool will analyze the message for phishing keywords,
psychological manipulation, suspicious links, and domain reputation.
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

    sentiment_score = get_sentiment(translated)
    if verbose:
        st.info(f"🧠 Sentiment Score: {sentiment_score:.2f}")

    detected = is_phishing(translated)

    urls = extract_urls(translated)
    if urls:
        st.write("🔗 URLs Found:")
        for url in urls:
            st.write("-", url)
            domain_rep = get_domain_reputation(url)
            if verbose:
                st.info(f"🌐 Domain Reputation for {url}: {domain_rep}")

    if detected:
        st.error("⚠️ This email is likely a PHISHING attempt.")
    else:
        st.success("✅ This email appears safe.")

    log_detection_result(translated, detected)
