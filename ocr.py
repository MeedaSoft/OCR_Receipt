import pytesseract
import cv2
import os
import tempfile
import numpy as np

# Set Tesseract path and tessdata directory
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"

def extract_text(image):
    """Extract text from image using Tesseract OCR with fallbacks"""
    if image is None or image.size == 0:
        print("Error: Image is empty or invalid")
        return ""
    
    # Ensure image is in proper format (uint8, 0-255)
    if image.dtype != np.uint8:
        image = np.uint8(image)
    
    # Convert to BGR if needed for proper handling
    if len(image.shape) == 2:  # Grayscale
        img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        img_bgr = image
    
    # Save to temporary JPEG file (more compatible than PNG)
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        temp_path = tmp.name
        try:
            cv2.imwrite(temp_path, img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            # Try with Thai + English first
            try:
                text = pytesseract.image_to_string(
                    temp_path,
                    lang="tha+eng",
                    config="--psm 6"
                )
                if text.strip():
                    return text
            except pytesseract.pytesseract.TesseractError as e:
                print(f"Thai+Eng OCR failed: {str(e)[:80]}...")
            
            # Fallback to English only
            try:
                print("Attempting English-only OCR...")
                text = pytesseract.image_to_string(
                    temp_path,
                    lang="eng",
                    config="--psm 6"
                )
                if text.strip():
                    return text
            except pytesseract.pytesseract.TesseractError as e:
                print(f"English OCR failed: {str(e)[:80]}...")
            
            # Try with German (since it's available)
            try:
                print("Attempting with German fallback...")
                text = pytesseract.image_to_string(
                    temp_path,
                    lang="deu",
                    config="--psm 6"
                )
                if text.strip():
                    print("(Note: German OCR was used)")
                    return text
            except pytesseract.pytesseract.TesseractError as e:
                print(f"German OCR failed: {str(e)[:80]}...")
            
            # Final fallback - try without language specification
            try:
                print("Attempting OCR with default settings...")
                text = pytesseract.image_to_string(
                    temp_path,
                    config="--psm 6"
                )
                return text if text.strip() else ""
            except Exception as e:
                print(f"All OCR attempts failed: {str(e)[:80]}...")
                return ""
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass  # Ignore cleanup errors
