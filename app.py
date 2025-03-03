from fastapi import FastAPI, File, UploadFile, HTTPException
import joblib
import os
import re

# Initialize FastAPI app
app = FastAPI()

# Define model and vectorizer paths
MODEL_PATH = "models/document_classifier.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

# Check if model and vectorizer exist
if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError("Model or vectorizer file not found.")

# Load the trained model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def extract_invoice_details(text: str):
    """Extract invoice details from text."""
    invoice_details = {
        "invoice_number": re.search(r"Invoice\s*No[:\s]*(\w+)", text, re.IGNORECASE),
        "date": re.search(r"Date[:\s]*(\d{2}/\d{2}/\d{4})", text),
        "amount": re.search(r"Total[:\s]*\$?([\d,]*\d+\.\d{2})", text)  # Added amount extraction
    }
    return {key: match.group(1) if match else None for key, match in invoice_details.items()}  # Fixed missing closing brace

@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to the document classification API!"}

@app.post("/classify_and_extract")
async def classify_and_extract(file: UploadFile = File(...)):
    """Classifies a document and extracts invoice details if applicable."""
    try:
        content = await file.read()
        text = content.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file format or encoding error.")
    
    # Preprocess and classify
    text_vectorized = vectorizer.transform([text])
    category = model.predict(text_vectorized)[0]
    
    result = {"category": category}
    
    if category == "invoices":
        result["invoice_details"] = extract_invoice_details(text)
    
    return result
