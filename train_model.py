import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

# Sample dataset
data = {
    'text': [
        "Your account has been suspended. Click here to verify.",
        "Update your payment details to continue using your service.",
        "Congratulations! You've won a $1000 gift card. Claim now.",
        "Meeting tomorrow at 10am in the conference room.",
        "Can you review the attached report and send your feedback?",
        "Happy birthday! Hope you have a great day!",
        "Your invoice is attached. Please review.",
        "Your Netflix subscription has been paused. Click to resume.",
        "Are we still on for lunch tomorrow?",
        "Alert: Suspicious login detected. Change your password immediately."
    ],
    'label': [1, 1, 1, 0, 0, 0, 0, 1, 0, 1]  # 1 = phishing, 0 = legitimate
}

# Load into DataFrame
df = pd.DataFrame(data)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Build pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

# Train model
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.2f}")

# Save model
joblib.dump(model, 'phishing_model.pkl')
print("Model saved as phishing_model.pkl")
