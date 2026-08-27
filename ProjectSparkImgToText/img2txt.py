import os
from datetime import datetime
import PyPDF2
from PIL import Image
import pytesseract


def img2txt(img_dir):
    files = [f for f in os.listdir(img_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    print(f"Imágenes encontradas: {len(files)}")
    if not files:
        print("No se encontraron imágenes en:", img_dir)
        return

    with open('/home/sion/projects/pyspark-training/image/docimg.txt', 'w+') as f:
        for img in files:
            start_time = datetime.now()
            input_img = os.path.join(img_dir, img)
            print("-" * 30)
            print(img)
            print("-" * 30)
            print("convirtiendo imagen " + img + "......")
            try:
                text = pytesseract.image_to_string(Image.open(input_img), lang='spa')
            except pytesseract.TesseractNotFoundError:
                print("ERROR: tesseract-ocr no está instalado o no está en el PATH")
                return
            print(text)
            f.write(img + "\n")
            f.write(text)
            print(f"Tiempo de conversión {img}: {datetime.now() - start_time}\n")


if __name__ == "__main__":
    img2txt("/home/sion/projects/pyspark-training/image")
