import os
import pytesseract
from PIL import Image
import cv2
import re
import numpy as np

# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_image(image_path):
    """Extracts text from an image using Tesseract OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def extract_emails(text):
    """Extracts email addresses from a given text."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, text)

def process_folder(folder_path):
    """Processes all images and emails in a given folder if not already extracted."""
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            text_file_path = os.path.splitext(image_path)[0] + ".txt"

            if os.path.exists(text_file_path):
                print(f"Skipping {filename}, already processed.")
                continue

            print(f"Processing: {image_path}")
            extracted_text = extract_text_from_image(image_path)
            emails = extract_emails(extracted_text)

            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write("Extracted Text:\n")
                text_file.write(extracted_text + "\n\n")
                text_file.write("Extracted Emails:\n")
                text_file.write("\n".join(emails) + "\n\n")
                text_file.write(f"Emails Processed: {', '.join(emails) if emails else 'None'}\n")

            print(f"Extraction complete! Saved text and emails to {text_file_path}")

        elif filename.endswith(".txt"):  # Process email extraction for text files
            text_file_path = os.path.join(folder_path, filename)
            with open(text_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                emails = extract_emails(content)
                print(f"Emails found in {filename}: {', '.join(emails) if emails else 'None'}")

# Process invoices, resumes, and email text files
process_folder("data/invoices")
process_folder("data/resumes")
process_folder("data/emails")
