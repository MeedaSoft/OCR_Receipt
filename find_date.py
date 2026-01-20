#!/usr/bin/env python3
"""Debug script to find date patterns"""

from preprocess import preprocess_image
from ocr import extract_text
import re

image = preprocess_image("img/receipt.jpg")
text = extract_text(image)

print("Looking for date/time patterns:")
for i, line in enumerate(text.split('\n')):
    if re.search(r'\d{2}[:/ -]\d{2}', line):
        print(f"Line {i}: {repr(line)}")
        print(f"  Actual: {line}")

print("\nAll lines with slashes:")
for i, line in enumerate(text.split('\n')):
    if '/' in line:
        print(f"Line {i}: {line}")
