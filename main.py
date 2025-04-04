import logging
from detector import is_phishing
from colorama import Fore, Style, init
import sys

# Initialize colorama
init(autoreset=True)

# Logging setup
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    print(Fore.CYAN + Style.BRIGHT + "=" * 43)
    print(Fore.MAGENTA + Style.BRIGHT + "     🛡️  AI PHISHING DETECTOR (v1.0)")
    print(Fore.CYAN + Style.BRIGHT + "=" * 43)

def main():
    display_banner()

    if len(sys.argv) > 1:
        email_input = ' '.join(sys.argv[1:])
        print(Fore.YELLOW + f"📂 File provided: {email_input}")
    else:
        print(Fore.YELLOW + "\n📩 Enter the email content to analyze:")
        email_input = input("> ")

    logging.info("Received email content.")

    if is_phishing(email_input):
        print(Fore.RED + Style.BRIGHT + "\n⚠️ This email is likely a PHISHING attempt.")
    else:
        print(Fore.GREEN + Style.BRIGHT + "\n✅ This email appears safe.")

if __name__ == "__main__":
    main()
