import re
import logging
import fitz  # PyMuPDF for PDF parsing
import extract_msg  # For .msg files
from langdetect import detect
from deep_translator import GoogleTranslator
from link_scanner import check_links

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

def is_phishing(content):
    logging.info("Received email content.")

    # Language Detection
    try:
        lang = detect(content)
        logging.info(f"🌐 Detected language: {lang}")
        if lang != 'en':
            content = GoogleTranslator(source=lang, target='en').translate(content)
            logging.info("🌍 Translated email content to English for analysis.")
    except Exception as e:
        logging.warning(f"🌐 Language detection failed: {e}")

    detected = False
    for keyword in PHISHING_KEYWORDS:
        if keyword in content.lower():
            logging.info(f"⚠️  Keyword matched: {keyword}")
            detected = True

    urls = extract_urls(content)
    if urls:
        logging.info(f"🔍 Found {len(urls)} URL(s). Scanning...")
        scan_results = check_links(urls)
        for url, status in scan_results.items():
            logging.info(f"🔗 {url} — {status}")
            if status == "🚨 Unsafe":
                detected = True
    else:
        logging.info("✅ No links found in the email.")

    return detected

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
