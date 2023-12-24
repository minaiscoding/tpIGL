import os
import requests
import logging
import validators
#--------------------------------------------------------------------------------------------------------------
from io import BytesIO
import spacy
import nltk
import re
#--------------------------------------------------------------------------------------------------------------
import PyPDF2
import fitz  # PyMuPDF
from pdfreader import PDFDocument
import pdfreader.viewer
import pdfminer
#--------------------------------------------------------------------------------------------------------------
from PIL import Image
import pytesseract
#--------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
#os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#-------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#///////////////////////
#    pdf_to_images 
#///////////////////////
def pdf_to_images(file_path):
    """Convert PDF pages to images."""
    pdf_document = fitz.open(file_path)
    
    images = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        image = page.get_pixmap()
        img = Image.frombytes("RGB", [image.width, image.height], image.samples)
        images.append(img)
    
    pdf_document.close()
    return images
#--------------------------------------------------------------------------------------------------------------
#//////////////////////////////////////////
#    extract_text_with_ocr from pdf images
#//////////////////////////////////////////
def extract_text_with_ocr(images):
    """Extract text using OCR from a list of images."""
    
    extracted_text = ''
    for image in images:
        # Perform OCR on the image using pytesseract
        text = pytesseract.image_to_string(image, lang='eng')
        extracted_text += text + '\n'  # Add newlines between pages
        extracted_text=clean_text(extracted_text)

    return extracted_text
#--------------------------------------------------------------------------------------------------------------
#///////////////////////
# column_boxes Function 
#///////////////////////
def column_boxes(page: fitz.Page, footer_margin: int = 0, no_image_text: bool = True) -> list:
    """Return list of column bounding boxes for the given page."""
#--------------------------------------------------------------------------------------------------------------
#////////////////////////////////
# extract_text_from_pdf Function
#////////////////////////////////
def clean_text(text):
    """
    Clean the extracted text by removing unwanted symbols and formatting.
    """
    # Remove special characters and symbols
    text = re.sub(r'[^a-zA-Z0-9\s\.,;:()\-–!?]','', text)
    
    return text

def extract_text_from_pdf(file_path):
    """
    Extract and organize text from a PDF file considering multi-column layout.

    Parameters:
        file_path (str): The path to the PDF file.

    Returns:
        str: Organized text with titles and paragraphs separated by newlines.
    """
    # Open the PDF file using PyMuPDF's fitz module.
    pdf_file = fitz.open(file_path)
    
    text = ''  # Initialize an empty string to store the extracted text.

    # Iterate through each page in the PDF file.
    for page_num in range(pdf_file.page_count):
        page = pdf_file[page_num]  # Get the current page.

        # Use the column_boxes function to detect column bounding boxes.
        bboxes = column_boxes(page, footer_margin=50, no_image_text=True)

        if bboxes:
            # If two columns are detected, extract text from each column separately.
            for rect in bboxes:
                # Use "blocks" mode to preserve text formatting
                blocks = page.get_text("blocks", clip=rect, sort=True)

                for b in blocks:
                    # Concatenate the text in each block along with its formatting
                    text += b[4] + '\n'
        else:
            # If only one column is present, extract text from the entire page.
            blocks = page.get_text("blocks")

            for b in blocks:
                text += b[4] + '\n'

    pdf_file.close()  # Close the PDF file.
    #text = clean_text(text)

    return text
#--------------------------------------------------------------------------------------------------------------
#//////////////////////////
#    extract_article_info 
#//////////////////////////
def extract_article_info(text):
    # Define regular expressions for each section
    title_pattern = re.compile(r'^\d+\s*(.*?)\n')
    authors_pattern = re.compile(r'\b(?:Dr|Prof|Mr|Mrs|Ms)\.?\s+(?:\w+\.?\s+)+\w+')
    institutions_pattern = re.compile(
        r'(?:Affiliation|Address|Dept|Department|School)\s*:\s*(.*?)\b(?:,|\.|$)|'
        r'\b(?:university|institute|laboratory|center|college|hospital|department|school|faculty)\b\s*(?:of|at|in)\s*(.*?)\b(?:,|\.|$)|'
        r'(?:Author )?[\w\s]+,\s*(.*?)\b(?:,|\.|$)'
    )
    abstract_pattern = re.compile(r'Abstract(.*?)Keywords', re.DOTALL)
    keywords_pattern = re.compile(r'Keywords (.*?)\.Introduction', re.DOTALL)
    references_pattern = re.compile(r'References(.*?)$', re.DOTALL)
    date_pattern = re.compile(
        r'Published:\s+(?P<date>\d{1,2}\s+[A-Z][a-z]{2,8}\s+\d{4})|'
        r"\d{4}-\d{2}-\d{2}|"
        r"\d{2}/\d{2}/\d{4}|"
        r"\d{1,2} [A-Z][a-z]{2,8} \d{4}",
        re.DOTALL
    )

    # Extract information using regular expressions
    title_match = title_pattern.search(text)
    authors_match = authors_pattern.search(text)
    institutions_match = institutions_pattern.search(text)
    abstract_match = abstract_pattern.search(text)
    keywords_match = keywords_pattern.search(text)
    references_match = references_pattern.search(text)
    date_match = date_pattern.search(text)

    # Get the matched groups
    title = title_match.group(1).strip() if title_match else None
    authors = authors_match.group(1).strip() if authors_match else None
    institutions = institutions_match.group().strip() if institutions_match else None
    abstract = abstract_match.group(1).strip() if abstract_match else None
    keywords = keywords_match.group(1).strip() if keywords_match else None
    references_text = references_match.group(1).strip() if references_match else None
    date = date_match.group().strip() if date_match else None

    # Split references based on the pattern (digit followed by a dot)
    references = re.split(r'\b\d+\.', references_text) if references_text else []

    # Remove empty references (if any)
    references = [ref.strip() for ref in references if ref.strip()]

    if not authors or not institutions:
        # If authors or institutions are not found using regex, use spaCy for entity recognition
        # Specify the number of lines to consider for entity recognition
        lines_for_entity_recognition = 20  # Adjust this based on the actual number of lines containing authors and institutions

        # Extract the relevant part of the text for entity recognition
        relevant_text = '\n'.join(text.split('\n')[:lines_for_entity_recognition])

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(relevant_text)

        # Extract authors using spaCy
        authors_entities = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]
        authors = ', '.join(authors_entities) if authors_entities else None

        # Extract institution using spaCy
        institution_entities = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        institutions = ', '.join(institution_entities) if institution_entities else None

    # Return a dictionary with extracted information
        
    article_info = {
        'title': title,
        'authors': authors,
        'institutions': institutions,
        'abstract': abstract,
        'keywords': keywords,
        'references': references,
        'date': date
    }
    print(title)
    print(authors)
    print(institutions)
    print(abstract)
    print(references)
    print(date)



    return article_info
#---------------------------------------------------------------------------------------------------

#////////////////////////
# download_pdf_from_url
#///////////////////////
def download_pdf_from_url(url):
    """
    Download a PDF from the given URL and save it to a local file.

    :param url: The URL of the PDF to be downloaded.
    :type url: str
    :return: The local file path if the download is successful, None otherwise.
    :rtype: str or None
    """
    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the response status code is 200 (HTTP OK)
    if response.status_code == 200:
        # Define the local file path to save the downloaded PDF
        local_file_path = 'downloaded_pdf.pdf'
        
        # Open the local file in binary write mode ('wb') and write the content of the response to it
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        
        # Return the local file path
        return local_file_path
    
    # Return None if the download was not successful
    return None










