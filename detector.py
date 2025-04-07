import re
import logging
import fitz  # PyMuPDF for PDF parsing
import extract_msg  # For .msg files
from langdetect import detect
from deep_translator import GoogleTranslator
from link_scanner import check_links
from textblob import TextBlob
import nltk
import os
from datetime import datetime

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Keyword list for phishing detection
PHISHING_KEYWORDS = [
    "verify", "account", "password", "login", "click here",
    "suspended", "update", "confirm", "urgent", "security alert",
    "reset your password", "bank", "limited time", "verify identity"
]

SUSPICIOUS_URL_KEYWORDS = [
    "login", "verify", "update", "secure", "account", "confirm", "password", "bank", "paypal"
]

URL_SHORTENERS = [
    "bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly", "buff.ly", "rebrand.ly"
]

# Social engineering phrases
SOCIAL_ENGINEERING_PHRASES = [
    "just wanted to check in", "can you do me a favor", "urgent but quick",
    "no need to worry", "you’ll love this opportunity", "you’ve been selected",
    "this stays between us", "I just need one thing from you", "you’re the only one who can help",
    "quick task for you", "need your input asap", "we're counting on you", "talk soon", "grab coffee",
    "hop on a quick call"
]

def is_phishing(content):
    logging.info("Received email content.")

    # Language Detection + Translation
    content = translate_to_english(content)

    detected = False
    threat_score = 0
    lower_content = content.lower()

    # Check for phishing keywords
    for keyword in PHISHING_KEYWORDS:
        if keyword in lower_content:
            logging.info(f"⚠️  Keyword matched: {keyword}")
            threat_score += 2
            detected = True

    # Check for social engineering phrases
    for phrase in SOCIAL_ENGINEERING_PHRASES:
        if phrase in lower_content:
            logging.info(f"🧠 Social engineering cue detected: {phrase}")
            threat_score += 2
            detected = True

    # Tone scoring
    try:
        sentiment = TextBlob(content).sentiment.polarity
        logging.info(f"🧠 Sentiment polarity: {sentiment:.2f}")
        if sentiment < -0.3:
            threat_score += 1
            detected = True
    except Exception as e:
        logging.warning(f"Sentiment analysis failed: {e}")

    # POS pattern matching
    try:
        sentences = nltk.sent_tokenize(content)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tags = nltk.pos_tag(words)
            if tags and tags[0][1].startswith("VB"):
                logging.info(f"🧠 POS pattern detected (starts with verb): {sentence}")
                threat_score += 1
                detected = True
    except Exception as e:
        logging.warning(f"POS tagging failed: {e}")

    # URL scanning
    urls = extract_urls(content)
    if urls:
        logging.info(f"🔍 Found {len(urls)} URL(s). Scanning...")
        scan_results = check_links(urls)
        for url, status in scan_results.items():
            logging.info(f"🔗 {url} — {status}")
            if status == "🚨 Unsafe":
                threat_score += 3
                detected = True
    else:
        logging.info("✅ No links found in the email.")

    return detected, min(threat_score, 10)  # Cap the score at 10

def extract_urls(text):
    return re.findall(r"https?://[^\s]+", text.lower())

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()

def extract_text_from_eml(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()

def extract_text_from_msg(file_path):
    try:
        msg = extract_msg.Message(file_path)
        return msg.body
    except Exception as e:
        logging.error(f"Failed to extract .msg: {e}")
        return ""

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        logging.error(f"Failed to extract .pdf: {e}")
        return ""

def extract_text_from_file(file_path):
    if file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    elif file_path.endswith(".eml"):
        return extract_text_from_eml(file_path)
    elif file_path.endswith(".msg"):
        return extract_text_from_msg(file_path)
    elif file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format")

def translate_to_english(text):
    try:
        detected_lang = detect(text)
        logging.info(f"🌐 Detected language: {detected_lang}")
        if detected_lang != "en":
            translated = GoogleTranslator(source=detected_lang, target="en").translate(text)
            logging.info("🌍 Translated email content to English for analysis.")
            return translated
        return text
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return text

def log_detection_result(content, is_phish, file_name=None):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = "PHISHING" if is_phish else "SAFE"
    fname = f"logs/detection_log.txt"
    with open(fname, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] - {file_name or 'Console Input'} ➜ {label}\n")
        f.write(f"{content}\n{'-'*40}\n")
