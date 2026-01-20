from preprocess import preprocess_image
from ocr import extract_text
from extractor import extract_data

IMAGE_PATH = "img/receipt.jpg"

def main():
    image = preprocess_image(IMAGE_PATH)
    text = extract_text(image)

    print("===== OCR TEXT =====")
    print(text)

    data = extract_data(text)
    print("\n===== EXTRACTED DATA =====")
    print(data)

if __name__ == "__main__":
    main()
