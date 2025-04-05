# 🛡️ AI Phishing Email Detector

# 🛡️ AI Phishing Email Detector

[![Streamlit App](https://ai-phishing-detector-8wtkg4vh45skksrablkq8w.streamlit.app/

A smart and simple tool to detect phishing threats in emails using keywords, ML models, and a sleek web interface.
## 🚀 Features

- 🔍 Detect phishing attempts from pasted text or uploaded `.txt` / `.eml` files
- 📊 Real-time keyword + ML detection
- 💻 Streamlit-based browser UI
- 💾 Log phishing keywords and events
- 🎯 Minimalist, fast, professional
🔄 **New in v1.1:** Now includes Light/Dark mode and upload UI!


---

## 🖥️ Screenshot

![UI Screenshot](demo_ui.png)

---
## 🖼️ PDF Upload Support

You can now upload `.pdf` files to analyze for phishing threats — in addition to `.txt` and `.eml`.

![PDF Upload Demo](demo_pdf.png)

## ⚙️ How to Run Locally

```bash
git clone https://github.com/Robair26/ai-phishing-detector.git
cd ai-phishing-detector
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
