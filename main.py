import sys
import logging
from detector import is_phishing
from extract import extract_email_body

logging.basicConfig(filename='log.txt', level=logging.INFO)

print("="*43)
print("     🛡️  AI PHISHING DETECTOR (v1.0)")
print("="*43)

if len(sys.argv) > 1:
    email_file = sys.argv[1]
    logging.info(f"📂 File provided: {email_file}")
    try:
        content = extract_email_body(email_file)
        print(f"\n📄 Extracted email content:\n{content}\n")
    except Exception as e:
        print("❌ Failed to extract email content:", str(e))
        sys.exit(1)
else:
    content = input("\n📩 Enter the email content to analyze:\n> ")

logging.info("Received email content.")

if is_phishing(content):
    print("\n⚠️ This email is likely a PHISHING attempt.")
else:
    print("\n✅ This email seems safe.")
