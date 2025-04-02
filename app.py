import streamlit as st
from detector import is_phishing

st.set_page_config(page_title="AI Phishing Email Detector", page_icon="🛡️")

st.markdown("""
    <h1 style='text-align: center;'>🛡️ AI Phishing Detector</h1>
    <p style='text-align: center;'>Paste or upload email content to detect phishing threats.</p>
    <hr>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📎 Upload Email (.txt, .eml, etc.):", type=["txt", "eml"])

email_text = ""

if uploaded_file is not None:
    email_text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.text_area("📨 Email Content:", value=email_text, height=250)

elif st.text_input("Or paste the email subject or message here:"):
    email_text = st.session_state.get("email_input", "")
    email_text = st.text_area("📨 Email Content:", value=email_text, height=250)

if st.button("🚀 Analyze"):
    if not email_text.strip():
        st.warning("⚠️ Please provide email content.")
    else:
        st.info("Analyzing...")
        if is_phishing(email_text):
            st.error("⚠️ This email is likely a PHISHING attempt.")
        else:
            st.success("✅ This email appears safe.")
