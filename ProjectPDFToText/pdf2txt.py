import os
from datetime import datetime
import pdfplumber


def pdf2txt(pdf_dir, output_path):
    files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    print(f"PDFs encontrados: {len(files)}")
    if not files:
        print("No se encontraron PDFs en:", pdf_dir)
        return

    with open(output_path, 'w+', encoding='utf-8') as out:
        for pdf in files:
            start_time = datetime.now()
            input_pdf = os.path.join(pdf_dir, pdf)
            print("-" * 30)
            print(pdf)
            print("-" * 30)
            print("convirtiendo pdf " + pdf + "......")

            try:
                text = ""
                with pdfplumber.open(input_pdf) as reader:
                    for page_num, page in enumerate(reader.pages, start=1):
                        page_text = page.extract_text() or ""
                        text += f"\n--- Página {page_num} ---\n" + page_text
            except Exception as e:
                print(f"ERROR procesando {pdf}: {e}")
                continue

            print(text)
            out.write(pdf + "\n")
            out.write(text)
            out.write("\n\n")
            print(f"Tiempo de conversión {pdf}: {datetime.now() - start_time}\n")


if __name__ == "__main__":
    pdf2txt("/home/sion/projects/pyspark-training/pdf",
            "/home/sion/projects/pyspark-training/pdf/docpdf.txt")