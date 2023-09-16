import re

from googletrans import Translator
import os
from os.path import join, splitext
import spacy
from PyPDF2 import PdfReader
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import imaplib
import pytesseract
from pytesseract import image_to_string
from PIL import Image
from io import BytesIO
#import fitz
from pdf2image import convert_from_path

translator = Translator()
def getLanguage(argument):
    switcher = {
        0: "en",
        5: "hi",
        4: "zh-CN",
        3: "ko",
        2: "ja"
    }
    return switcher.get(argument, "en")  # Default to English if the option is not found

"""print("0.ENGLISH")
print("5.HINDI")
print("4.chinese")
print("3.KOREAN")
print("2.JAPANESE")
txt = int(input("select a language to enter the text: "))"""
print("0.ENGLISH")
print("5.HINDI")
print("4.chinese")
print("3.KOREAN")
print("2.JAPANESE")
#byte_array = content.encode('utf-8')

# Translate the content using the Google Translate API
# Change this to your desired target language code
tran = int(input("select a language to convert in: "))
lang = getLanguage(tran)
print(lang)


current_dir = os.getcwd()
#print("Current Directory:", current_dir)
# Change the current working directory to the desired folder
os.chdir(r'D:\test2')
# Access a specific folder within the current directory
target_folder = join(current_dir, r'D:\test2')
print("Target Folder Path:", target_folder)
# List files and subdirectories within a folder
file_list = os.listdir(target_folder)
print("Files in Target Folder:", file_list)
stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
content = ""
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'
for i in file_list:
    s = r"D:\test2\{}".format(i)
    def get_file_extension(s):
        return splitext(s)[1][1:]  # Remove the leading dot
    # Example usage:
    extension = get_file_extension(s)
    # print("File extension:", extension)
    # Load the Word document
    if (extension == 'pdf'):


        def check_pdf_content(pdf_path):
            has_text = False
            has_images = False
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                # Check if the PDF contains text
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text.strip():  # Check if the extracted text is not empty
                        has_text = True
                        break
                # Check if the PDF contains images
                if '/XObject' in page['/Resources']:
                    xObject = page['/Resources']['/XObject'].get_object()
                    if xObject:
                        for obj in xObject:
                            if xObject[obj]['/Subtype'] == '/Image':
                                has_images = True
                                break
                """for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    xObject = page['/Resources']['/XObject'].get_object()
                    if xObject is not None:
                        for obj in xObject:
                            if xObject[obj]['/Subtype'] == '/Image':
                                has_images = True
                                break"""
            return has_text, has_images


        if __name__ == "__main__":
            text_present, images_present = check_pdf_content(s)

            if text_present:
                # If the page has text, extract it directly
                with open(s, 'rb') as pdf_file:
                    # Create a PDF reader object
                    pdf = PdfReader(pdf_file)
                    # Get the number of pages in the PDF
                    num_pages = len(pdf.pages)
                    # Extract text from all pages and store it in the 'text' variable
                    content: str = ""
                    page_content = ""
                    for page_num in range(num_pages):
                        page = pdf.pages[page_num]
                        content += page.extract_text()
                        page_content += content
                        preprocessed_content = re.sub(r'\s+', ' ', page_content).strip
                        translated_text = translator.translate(page_content, dest=lang)
                        print(translated_text.text)
                # print("The PDF contains text.")

            elif images_present:
                # Open the PDF file and read its content using PyPDF2
                """with open(s, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    # Iterate through all pages
                    for page_num in range(len(pdf_reader.pages)):
                        # Convert the page to an image using pdf2image
                        images = convert_from_path(s, first_page=page_num + 1, last_page=page_num + 1,
                                                   poppler_path=r'D:\poppler-23.07.0\Library\bin')
                        # Save each image to the output folder
                        for idx, image in enumerate(images):
                            image_path = join(f"page{page_num + 1}_image{idx + 1}.jpg")
                            img = image.save(image_path, 'JPEG')
                            extracted_text = pytesseract.image_to_string(Image.open(image_path))
                            if not extracted_text:
                                print("No text extracted from the image.")
                                exit()
                            content += extracted_text + "\n" """
                with open(s, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)

                    # Iterate through all pages
                    for page_num in range(len(pdf_reader.pages)):
                        # Convert the page to an image using pdf2image
                        images = convert_from_path(s, first_page=page_num + 1, last_page=page_num + 1,
                                                   poppler_path=r'D:\poppler-23.07.0\Library\bin')
                        # Initialize the page_content variable to store text extracted from this page
                        page_content = ""

                        # Iterate through images on this page and perform OCR
                        for idx, image in enumerate(images):
                            image_path = join(f"page{page_num + 1}_image{idx + 1}.jpg")
                            img = image.save(image_path, 'JPEG')
                            extracted_text = pytesseract.image_to_string(Image.open(image_path))
                            """if not extracted_text:
                                print("No text extracted from the image.")
                                exit()"""
                            page_content += extracted_text
                            preprocessed_content = re.sub(r'\s+', ' ', page_content).strip
                            translated_text = translator.translate(page_content, dest=lang)
                            print(translated_text.text)
                                # You can choose to continue with the next page or take other actions as needed
                            # Append the extracted text from this image to the page_content
                            """page_content += extracted_text
                            preprocessed_content = re.sub(r'\s+', ' ', page_content).strip
                            translated_text = translator.translate(page_content, dest=lang)
                            print(translated_text.text)"""

                        # Append the page_content to the overall content
                        #content += page_content

                # Check if content is empty or None before attempting translation
                """if not content:
                    print("No text content found for translation.")
                    exit()"""
                #preprocessed_content = re.sub(r'\s+', ' ', content).strip()

                # Check if preprocessed content is empty or None before attempting translation
                """if not preprocessed_content:
                    print("No text content found for translation.")
                    exit()"""

                #preprocessed_content_str = str(preprocessed_content)

                #preprocessed_content = re.sub(r'\s+', ' ', content).strip()

                """byte_array = bytearray()

                for char in preprocessed_content:
                    if char == ' ':
                        byte_array.append(32)  # Append ASCII value of space
                    else:
                        byte_array.append(ord(char))
                content = byte_array"""
            """ print("0.ENGLISH")
            print("5.HINDI")
            print("4.chinese")
            print("3.KOREAN")
            print("2.JAPANESE")
            #byte_array = content.encode('utf-8')

            # Translate the content using the Google Translate API
            # Change this to your desired target language code
            tran = int(input("select a language to convert in: "))
            lang = getLanguage(tran)
            print(lang)
            translated_text = translator.translate(content, dest=lang)
            print(translated_text.text)"""
        """except Exception as e:
            print("Translation failed. Please try again later.")
            print(f"Error: {e}")"""

"""print("0.ENGLISH")
print("5.HINDI")
print("4.chinese")
print("3.KOREAN")
print("2.JAPANESE")
txt = int(input("select a language to enter the text: "))
"""


"""print("0.ENGLISH")
print("5.HINDI")
print("4.chinese")
print("3.KOREAN")
print("2.JAPANESE")
tran = int(input("select a language to convert in: "))
lang = getLanguage(tran)
print(lang)
translated_text = translator.translate(content, dest=lang)
print(translated_text.text)"""