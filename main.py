import PyPDF2
import fitz
import io
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path


# Set path to directory containing PDF files
pdf_dirs = r'C:\Users\566a5\PycharmProjects\Работа\scan_documents\ДОГОВОРА'

# Set path to directory where JPG files will be saved
output_dir = r'C:\Users\566a5\PycharmProjects\Работа\scan_documents\jpgs'


def extract_images(pdf_path, output_dir):
    print(pdf_path)
    doc = fitz.open(pdf_path)
    name_dir = pdf_path.split('\\')[-2]
    name_doc = pdf_path.split('\\')[-1]
    new_dir = str(output_dir) + '\\' + name_dir
    if os.path.isdir(new_dir):
        pass
    else:
        os.mkdir(new_dir)

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Identity, dpi=300,
                              colorspace=fitz.csRGB, clip=None, alpha=True, annots=True)
        name_jpg = f'{name_doc.replace(".pdf", "")}-{page.number}.jpg'
        pix.save(os.path.join(new_dir, name_jpg))


# Loop through all PDF files in directory
def scraping_all_pdf():
    for folder in os.listdir(pdf_dirs):
        full_path = os.path.join(pdf_dirs, folder)
        print(full_path)
        for pdf_file in os.listdir(full_path):
            # Check if file is a PDF
            if pdf_file.endswith('.pdf'):
                print(pdf_file)
                # Set path to PDF file
                pdf_path = os.path.join(full_path, pdf_file)

                # Extract images from PDF and save as JPGs
                extract_images(pdf_path, output_dir)
        break


def extract_text_from_image():
    folders = os.listdir(output_dir)
    # print(images)
    for folder in folders:
        full_path = os.path.join(output_dir, folder)
        print(full_path)
        for image in os.listdir(full_path):
            print(image)
            full_path_images = os.path.join(full_path, image)
            image = Image.open(full_path_images)

            # Set the Tesseract configuration to use the Russian language
            config = '-l rus tessedit_char_whitelist=0123456789'
            pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            # Extract text from the image
            text = pytesseract.image_to_string(image, config=config)

            # Print the extracted text
            print(text)
        break



def main():
    # scraping_all_pdf()
    extract_text_from_image()


if __name__ == '__main__':
    main()
