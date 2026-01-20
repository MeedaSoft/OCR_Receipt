#!/usr/bin/env python3
"""Diagnostic script to check OCR setup"""

import os
import sys
import cv2
import pytesseract
import shutil
import subprocess
from io import StringIO

def suppress_stderr(func):
    """Decorator to suppress stderr during function execution"""
    def wrapper(*args, **kwargs):
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        try:
            return func(*args, **kwargs)
        finally:
            sys.stderr = old_stderr
    return wrapper

def check_tesseract():
    """Check Tesseract installation"""
    print("=" * 60)
    print("TESSERACT DIAGNOSIS")
    print("=" * 60)
    
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    if os.path.exists(tesseract_path):
        print(f"✓ Tesseract found at: {tesseract_path}")
    else:
        print(f"✗ Tesseract NOT found at: {tesseract_path}")
        print("\nSearching for Tesseract...")
        result = shutil.which("tesseract")
        if result:
            print(f"  Found at: {result}")
        else:
            print("  Not found in PATH")
        return False
    
    # Check version - use subprocess to avoid pytesseract's stderr warnings
    try:
        result = subprocess.run([tesseract_path, '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0] if result.stdout else "Unknown"
            print(f"✓ Tesseract version: {version_line}")
        else:
            print(f"⚠️  Tesseract found but version check had issues")
    except Exception as e:
        print(f"⚠️  Could not determine version, but Tesseract is installed")
    
    return True

def check_languages():
    """Check available languages"""
    print("\n" + "=" * 60)
    print("LANGUAGE DATA CHECK")
    print("=" * 60)
    
    # Set tesseract path first
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    try:
        langs = pytesseract.get_languages()
        print(f"Available languages: {langs}")
        
        if 'eng' in langs:
            print("✓ English (eng) available")
        else:
            print("✗ English (eng) NOT available")
        
        if 'tha' in langs:
            print("✓ Thai (tha) available")
        else:
            print("✗ Thai (tha) NOT available - Install from https://github.com/UB-Mannheim/tesseract/wiki")
    except Exception as e:
        print(f"✗ Error checking languages: {str(e)[:80]}")
        return False
    
    return True

def check_image():
    """Check if test image exists and is readable"""
    print("\n" + "=" * 60)
    print("IMAGE FILE CHECK")
    print("=" * 60)
    
    image_path = os.path.join(os.path.dirname(__file__), "img/receipt.jpg")
    
    if os.path.exists(image_path):
        print(f"✓ Image found at: {image_path}")
        
        # Try to read with OpenCV
        try:
            img = cv2.imread(image_path)
            if img is not None:
                height, width = img.shape[:2]
                print(f"✓ Image readable: {width}x{height} pixels")
            else:
                print("✗ Image not readable by OpenCV")
                return False
        except Exception as e:
            print(f"✗ Error reading image: {e}")
            return False
    else:
        print(f"✗ Image NOT found at: {image_path}")
        return False
    
    return True

def main():
    print("\nOCR System Diagnostic Tool\n")
    
    results = {
        "Tesseract": check_tesseract(),
        "Languages": check_languages(),
        "Image": check_image(),
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test}")
    
    if not all(results.values()):
        print("\n⚠️  Some issues detected. See above for details.")
        sys.exit(1)
    else:
        print("\n✓ All checks passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
