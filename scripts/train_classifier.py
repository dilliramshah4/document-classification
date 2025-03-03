import os
import pandas as pd
import re
import joblib
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Paths
DATA_DIR = "data"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)  # Ensure 'models' directory exists

# Function to Load Data
def load_data():
    texts = []
    labels = []
    for category in os.listdir(DATA_DIR):
        category_path = os.path.join(DATA_DIR, category)
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                file_path = os.path.join(category_path, filename)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    texts.append(f.read())
                    labels.append(category)
    return texts, labels

# Preprocessing Function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text

# Load & Preprocess Data
texts, labels = load_data()
texts = [preprocess_text(text) for text in texts]

# Convert text to numerical features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
y = labels

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate Model
predictions = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

# Save Model & Vectorizer in 'models' directory
joblib.dump(model, os.path.join(MODEL_DIR, "document_classifier.pkl"))
joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))

print(f"✅ Model saved at {MODEL_DIR}/document_classifier.pkl")
print(f"✅ Vectorizer saved at {MODEL_DIR}/vectorizer.pkl")
