# OCR System Setup and Troubleshooting Guide

## Current Status
✓ Image file loads correctly (1152x2048 pixels)
✗ Tesseract executable found but **NOT WORKING** - Not in PATH or corrupted installation

## Root Cause
Your Tesseract installation has issues:
1. Tesseract file exists at `C:\Program Files\Tesseract-OCR\tesseract.exe` 
2. BUT pytesseract cannot access it properly (PATH issue or installation corruption)
3. Thai language data may be missing (tha.traineddata)

## Solutions (Try in order)

### Solution 1: Fix PATH Environment Variable (Recommended)
1. **Open Environment Variables:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click "Environment Variables" button
   - Under "System variables", find "Path"
   - Click "Edit"

2. **Add Tesseract to PATH:**
   - Click "New"
   - Add: `C:\Program Files\Tesseract-OCR\Tesseract-OCR\bin`
   - Click OK on all dialogs
   - **Restart your terminal/IDE**

3. **Verify it works:**
   ```bash
   python diagnose.py
   ```

### Solution 2: Reinstall Tesseract (If Solution 1 doesn't work)
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Download: `tesseract-ocr-w64-setup-v5.x.x.exe` (latest version)
3. Run installer with:
   - **Check "Add to PATH" during installation**
   - Install all language packs you need

4. **Verify installation:**
   ```bash
   python diagnose.py
   ```

### Solution 3: Install Thai Language Data (After fixing Tesseract)
Once Tesseract works, add Thai language support:

1. Download `tha.traineddata` from:
   https://github.com/UB-Mannheim/tesseract/wiki
   
2. Place it in:
   `C:\Program Files\Tesseract-OCR\tessdata\`

3. Verify with diagnostic:
   ```bash
   python diagnose.py
   ```

## Quick Fixes to Try First

### Check if Tesseract is in PATH:
```bash
where tesseract
```
If nothing is returned, Tesseract is not in PATH.

### Force Tesseract path (Temporary Fix):
Edit `ocr.py` line 6:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```
This is already set, but make sure the path is correct for your installation.

## Code Improvements Made

Your code has been updated with:

1. **Better Image Preprocessing** (`preprocess.py`):
   - Auto-scaling for small images
   - CLAHE contrast enhancement
   - Denoising for clearer text
   - Morphological operations
   - Better threshold computation

2. **Robust OCR with Fallbacks** (`ocr.py`):
   - Multiple language attempts (Thai+Eng → Eng → default)
   - Proper error handling
   - Temp file workaround for image format issues
   - Graceful degradation

3. **Diagnostic Tool** (`diagnose.py`):
   - Checks Tesseract installation
   - Lists available languages
   - Verifies image file readability

## Testing Your Setup

Once you fix Tesseract:

1. Run diagnostic:
   ```bash
   python diagnose.py
   ```
   Should show ✓ for all items

2. Run OCR:
   ```bash
   python main.py
   ```
   Should extract text from the receipt image

## What To Do Now

1. **First**: Check if Tesseract is in PATH:
   ```bash
   where tesseract
   ```

2. **If not found**: Run Solution 1 (add to PATH)

3. **If still not working**: Run Solution 2 (reinstall)

4. **If Tesseract works but no Thai**: Run Solution 3 (install Thai data)

5. **Verify**: Run `python diagnose.py` to confirm everything is fixed

---
Generated: 2026-01-21
