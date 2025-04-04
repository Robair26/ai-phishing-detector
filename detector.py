import re
import logging

PHISHING_KEYWORDS = [
    "verify", "suspend", "login", "update", "account", "click here", "password",
    "urgent", "immediately", "limited time", "alert", "confirm"
]

SUSPICIOUS_LINK_PATTERN = r'https?:\/\/[^ ]*'

def is_phishing(text):
    text_lower = text.lower()
    found_keywords = []

    for keyword in PHISHING_KEYWORDS:
        if keyword in text_lower:
            logging.info(f"⚠️  Keyword matched: {keyword}")
            found_keywords.append(keyword)

    if re.search(SUSPICIOUS_LINK_PATTERN, text_lower):
        logging.info("⚠️  Suspicious link found.")
        found_keywords.append("link")

    return bool(found_keywords)
