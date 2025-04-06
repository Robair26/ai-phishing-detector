import sys
from detector import (
    is_phishing,
    extract_text_from_file,
    log_threat_result  # ✅ NEW IMPORT
)

print("===========================================")
print("     🛡️  AI PHISHING DETECTOR (v1.0)")
print("===========================================")

# Determine source of input
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    print(f"\n📂 File provided: {file_path}")
    try:
        content = extract_text_from_file(file_path)
        source = file_path
    except Exception as e:
        print(f"\n❌ Failed to extract email content: {e}")
        sys.exit(1)
else:
    content = input("\n📩 Enter the email content to analyze:\n> ")
    source = "Manual Input"

# Run phishing detection
is_phish = is_phishing(content)

# Result display
if is_phish:
    print("\n⚠️ This email is likely a PHISHING attempt.")
else:
    print("\n✅ This email appears safe.")

# ✅ Log to file
log_threat_result(content, is_phish, source)
