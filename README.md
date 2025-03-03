# Document Classification & Invoice Data Extraction API

## Overview

This project implements a document classification and invoice data extraction API using FastAPI. The system classifies uploaded documents into predefined categories (e.g., invoice, receipt, report) and, if classified as an invoice, extracts key fields and table data using OCR (Tesseract).

## Features

- ✅ Document Classification - Categorizes documents into predefined classes.
- ✅ Invoice Data Extraction - Extracts invoice number, date, amount, vendor details, and tabular data.
- ✅ OCR Integration - Uses Tesseract OCR to process image-based invoices.
- ✅ REST API with FastAPI - Provides endpoints to upload and classify documents.
- ✅ Structured Output - Returns extracted data in JSON format.

## Task Breakdown

### 1️⃣ Dataset Exploration & Preprocessing

- Download dataset from Kaggle.
- Analyze and clean data (handling missing values, invalid entries, duplicates).
- Prepare dataset for training/testing with proper labels.

### 2️⃣ Document Classification Service

- Train a machine learning model to classify documents (e.g., invoice, receipt, resumes).
- Evaluate model performance using metrics like accuracy and F1-score.

### 3️⃣ Invoice Data Extraction

- Extract fields like invoice number, date, amount, vendor details.
- Extract tabular data (item descriptions, quantities, prices) and store in JSON/CSV.
- Use Tesseract OCR for image-based invoice processing.

### 4️⃣ Deployment-Ready API

- FastAPI framework for building the REST API.
- Endpoint: `/classify_and_extract` to classify and extract invoice data.
- Handle file uploads and return structured JSON output.

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip package manager
- Tesseract OCR (for image-based text extraction)

### Steps

1. Install required packages:
    ```sh
    pip install -r requirements.txt
    ```
2. Run the API:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

## API Endpoints

| Method | Endpoint               | Description                                           |
|--------|------------------------|-------------------------------------------------------|
| POST   | /classify_and_extract  | Uploads document, classifies it, and extracts relevant data. |

### Example Usage (cURL):
```sh
curl -X 'POST' 'http://localhost:8000/classify_and_extract' \
     -F 'file=@invoice.txt'
```

## Model Details

- **Algorithm**: Uses Machine Learning (Naïve Baye) for document classification.
- **OCR Integration**: Extracts text from images using Tesseract OCR.
- **Data Preprocessing**: Uses tokenization, stopword removal, and TF-IDF vectorization.



## Deliverables

- ✔ Codebase: Well-structured, documented Python code.
- ✔ Instructions: Clear steps to set up and run locally.
- ✔ Model Explanation: Brief details on classification and extraction techniques.
- ✔ Evaluation Report: Metrics and optimizations applied.
- ✔ Demo Video: Short walkthrough showcasing the API in action.

## Demo Video

[Watch the demo video](https://drive.google.com/file/d/1C9kl21uNLhhLC4wGmxCV-fotrZArTDX3/view?usp=sharing)
