#!/usr/bin/env python3
"""Debug script to analyze OCR output and test extraction"""

from preprocess import preprocess_image
from ocr import extract_text
from extractor import extract_data

IMAGE_PATH = "img/receipt.jpg"

def main():
    image = preprocess_image(IMAGE_PATH)
    text = extract_text(image)
    
    print("===== RAW OCR TEXT =====")
    print(repr(text[:500]))  # Show first 500 chars with repr to see actual characters
    print("\n===== LOOKING FOR NUMBERS =====")
    
    import re
    numbers = re.findall(r'[0-9,.\s]+', text)
    print(f"Found numbers: {numbers[:10]}")
    
    print("\n===== LINES WITH NUMBERS =====")
    for i, line in enumerate(text.split('\n')):
        if re.search(r'\d', line):
            print(f"Line {i}: {line[:80]}")
    
    print("\n===== EXTRACTED DATA =====")
    data = extract_data(text)
    print(data)

if __name__ == "__main__":
    main()
