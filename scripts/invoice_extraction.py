import os
import re
import json
import pandas as pd
from pytesseract import image_to_string
from PIL import Image

def extract_invoice_fields(text):
    """Extract key fields from invoice text."""
    invoice_number = re.search(r'Invoice\s*No[:\s]+(\S+)', text, re.IGNORECASE)
    date = re.search(r'Date[:\s]+(\S+)', text, re.IGNORECASE)
    amount = re.search(r'Total[:\s]+([\d,.]+)', text, re.IGNORECASE)
    vendor = re.search(r'Vendor[:\s]+(.+)', text, re.IGNORECASE)
    
    return {
        "invoice_number": invoice_number.group(1) if invoice_number else None,
        "date": date.group(1) if date else None,
        "amount": amount.group(1) if amount else None,
        "vendor": vendor.group(1) if vendor else None
    }

def extract_table_data(text):
    """Extract table-like structures from invoice text."""
    lines = text.split('\n')
    table_data = []
    
    for line in lines:
        columns = re.split(r'\s{2,}', line)
        if len(columns) >= 3:  # Ensure a valid table row with at least 3 columns
            table_data.append(columns)
    
    return pd.DataFrame(table_data, columns=["Item", "Quantity", "Price"]) if table_data else None

def process_invoice(image_path, output_dir):
    """Process a single invoice image and extract data."""
    text = image_to_string(Image.open(image_path))
    extracted_data = extract_invoice_fields(text)
    table_df = extract_table_data(text)
    
    invoice_name = os.path.basename(image_path).split('.')[0]
    
    # Save extracted fields as JSON
    json_path = os.path.join(output_dir, f"{invoice_name}.json")
    with open(json_path, 'w') as f:
        json.dump(extracted_data, f, indent=4)
    
    # Save table data as CSV if available
    if table_df is not None:
        csv_path = os.path.join(output_dir, f"{invoice_name}.csv")
        table_df.to_csv(csv_path, index=False)
    
    print(f"Processed: {image_path}")

def main():
    input_dir = "data/invoices"
    output_dir = "extracted_data/invoices"
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif')):
            process_invoice(os.path.join(input_dir, filename), output_dir)
    
if __name__ == "__main__":
    main()

    import json

output_file = "data/invoices/extracted_invoices.json"

with open(output_file, "w") as f:
    json.dump(extracted_data, f, indent=4)

print(f"Extracted data saved to {output_file}")

