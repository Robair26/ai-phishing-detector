from detector import is_phishing

def test_phishing_detection():
    phishing_email = "Click here to verify your account now!"
    assert is_phishing(phishing_email) == True

    safe_email = "Meeting is scheduled for 10 AM tomorrow."
    assert is_phishing(safe_email) == False

if __name__ == "__main__":
    test_phishing_detection()
    print("✅ All tests passed.")
