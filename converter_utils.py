import fitz
import docx2txt
import base64
import io
import pdf2image
import os
import glob
def convert_pdf_to_images(filepath: str, output: str = None):
    doc = fitz.open(filepath)
    page = doc.load_page(0)  # number of page
    pix = page.get_pixmap()
    pix.save(output)
    doc.close()

def extract_docx(file_path: str):
    text = docx2txt.process(file_path)
    return text
def pdf_to_base64_images(pdf_file):
    """
    Converte un PDF in una lista di immagini base64.

    Args:
      pdf_file: Il percorso del file PDF da convertire.

    Returns:
      Una lista di stringhe base64, ognuna delle quali rappresenta una pagina del PDF.
    """

    with open(pdf_file, "rb") as f:
        pdf = pdf2image.convert_from_bytes(f.read())

    base64_images = []
    for page in pdf:
        buf = io.BytesIO()
        page.save(buf, format="PNG")
        base64_images.append(base64.b64encode(buf.getvalue()).decode())

    return base64_images

# image_content = image_file.read()
# base64_image = base64.b64encode(image_content).decode('utf-8')


def svuota_cartella(cartella):
    files = glob.glob(os.path.join(cartella, '*'))
    for f in files:
        os.remove(f)



if __name__ == '__main__':
    # Esempio di utilizzo
    pdf_file = "../Resources/attention_is_all_you_need.pdf"
    base64_images = pdf_to_base64_images(pdf_file)
    # Stampa la lista delle immagini base64
    for base64_image in base64_images:
        print(base64_image)