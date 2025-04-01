import logging
import re

# 🎨 Set up logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# 🎯 Keywords and pattern to look for
PHISHING_KEYWORDS = [
    "password", "verify", "urgent", "login", "click here", "account", "update",
    "suspended", "limited", "credit card", "ssn", "social security", "bank", "confirm"
]

SUSPICIOUS_LINK_PATTERN = r'https?:\/\/[^ ]+'

def is_phishing(text):
    text_lower = text.lower()
    is_flagged = False

    # 🔍 Keyword matching
    for keyword in PHISHING_KEYWORDS:
        if keyword in text_lower:
            logging.info(f"⚠️  Keyword matched: {keyword}")
            is_flagged = True

    # 🔗 Suspicious link detection
    links_found = re.findall(SUSPICIOUS_LINK_PATTERN, text)
    if links_found:
        for link in links_found:
            logging.info(f"🔗 Suspicious link detected: {link}")
        is_flagged = True

    return is_flagged
