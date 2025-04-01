import logging
from detector import is_phishing
from datetime import datetime

# 🎨 Color codes for console
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# 🖥️ CLI Banner
print(f"""{YELLOW}
===========================================
     🛡️  AI PHISHING DETECTOR (v1.0)      
===========================================
{RESET}""")

# 📨 Get email input
email = input("📩 Enter the email content to analyze:\n> ")
logging.info("Received email content.")

# 🤖 Run detection
result = is_phishing(email)

# 🎯 Display result with color
if result:
    print(f"{RED}\n⚠️ This email is likely a PHISHING attempt.\n{RESET}")
else:
    print(f"{GREEN}\n✅ This email appears to be SAFE.\n{RESET}")
