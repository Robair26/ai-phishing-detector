import sys
import logging
from detector import (
    is_phishing,
    extract_text_from_txt,
    extract_text_from_eml,
    extract_text_from_msg,
    extract_text_from_pdf
)

logging.basicConfig(level=logging.INFO)

print("===========================================")
print("     🛡️  AI PHISHING DETECTOR (v1.0)")
print("===========================================")

email_content = ""

# Handle file input
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    logging.info(f"📂 File provided: {file_path}")

    if file_path.endswith(".txt"):
        email_content = extract_text_from_txt(file_path)
    elif file_path.endswith(".eml"):
        email_content = extract_text_from_eml(file_path)
    elif file_path.endswith(".msg"):
        email_content = extract_text_from_msg(file_path)
    elif file_path.endswith(".pdf"):
        email_content = extract_text_from_pdf(file_path)
    else:
        logging.error("❌ Unsupported file format.")
        sys.exit(1)

    if not email_content:
        print("❌ Failed to extract content from the file.")
        sys.exit(1)

else:
    email_content = input("\n📩 Enter the email content to analyze:\n> ")

# Detect phishing
if is_phishing(email_content):
    print("\n⚠️ This email is likely a PHISHING attempt.")
else:
    print("\n✅ This email appears safe.")
