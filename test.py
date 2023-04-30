import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import os

if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

file = 'MR - MRI Report.pdf'
text = ""
pdf_file = open(file, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
for page in pdf_reader.pages:
    text += page.extract_text()
pdf_file.close()

# remove all whitespaces and newlines
text = text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')

if text == "":
    print("No text found, trying OCR...")
    # extract images from pdf
    images = convert_from_path(file)
    for image in images:
        # extract text from image
        text += pytesseract.image_to_string(image)

print(text)