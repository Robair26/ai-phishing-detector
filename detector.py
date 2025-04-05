import joblib
import string
import re

# Load trained model
model = joblib.load("phishing_model.pkl")

# Optional: clean text before prediction
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_phishing(email_text):
    clean_text = preprocess(email_text)
    prediction = model.predict([clean_text])[0]
    probability = model.predict_proba([clean_text])[0][prediction]
    return prediction, probability
