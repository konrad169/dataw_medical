from PyPDF2 import PdfFileWriter, PdfFileReader, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image
import os
import streamlit as st


def create_pdf_with_logo_and_text(logo_path, text, output_path):
    packet = BytesIO()
    path = str(os.path.abspath(os.getcwd())) + "/"
    c = canvas.Canvas(packet, pagesize=letter)
    with Image.open(logo_path) as logo:
        logo_resized = logo.resize((200, 150), Image.LANCZOS)
        logo_path_resized = f"{path}assets/logo_dw_resized.png"
        logo_resized.save(logo_path_resized)
    # Posiziona il logo in alto a sinistra
    c.drawImage(logo_path_resized, 10, 650)  # Cambia le coordinate come necessario
    # Inserisci il testo subito dopo il logo
    text_object = c.beginText(10, 670)  # Cambia le coordinate come necessario
    for line in text.splitlines():
        text_object.textLine(line)
    c.drawText(text_object)  # Cambia le coordinate come necessario
    c.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    output = PdfWriter()
    # Aggiungi il logo e il testo a tutte le pagine
    for i in range(len(new_pdf.pages)):
        page = new_pdf.pages[i]
        output.add_page(page)
    with open(output_path, "wb") as f:
        output.write(f)

# Crea un PDF con il testo


# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet
#
#
# def create_pdf_with_logo_and_text_2(logo_path, text_list, output_path):
#     # Crea un nuovo documento PDF
#     doc = SimpleDocTemplate(output_path, pagesize=letter)
#
#     # Carica gli stili predefiniti
#     styles = getSampleStyleSheet()
#     style = styles['Normal']
#
#     # Posiziona il logo in alto a sinistra
#     logo = Image(logo_path, width=200, height=31)
#     logo.hAlign = 'LEFT'
#
#     # Crea una lista per contenere gli elementi del PDF
#     elements = [logo]
#
#     # Aggiungi il testo al PDF, creando una nuova pagina per ogni elemento in text_list
#
#     paragraph = Paragraph(text_list, style)
#     elements.append(paragraph)
#     elements.append(PageBreak())  # Crea una nuova pagina
#
#     # Costruisci il PDF
#     doc.build(elements)

#
# create_pdf_with_logo_and_text("assets/DataWizard.png", "Il tuo testo qui. Alessio è un cane di merda. Valerio è bellissimo.\n"
#                      "Corrado è il re supremo dell'universo", "output.pdf")