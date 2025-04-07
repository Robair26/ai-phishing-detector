import sys
import logging
from detector import (
    is_phishing,
    extract_text_from_file,
    translate_to_english,
    extract_urls,
    log_detection_result
)

# Logging setup (for terminal output)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

print("=" * 43)
print("     🛡️  AI PHISHING DETECTOR (v1.0)")
print("=" * 43)

# Get input (file or manual)
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    print(f"\n📂 File provided: {file_path}")
    try:
        email_content = extract_text_from_file(file_path)
    except Exception as e:
        print(f"\n❌ Failed to extract email content: {e}")
        sys.exit(1)
else:
    email_content = input("\n📩 Enter the email content to analyze:\n> ")

# Process the email
is_phish = is_phishing(email_content)

# Log result
log_detection_result(email_content, is_phish)

# Show result
if is_phish:
    print("\n⚠️ This email is likely a PHISHING attempt.")
else:
    print("\n✅ This email appears safe.")
