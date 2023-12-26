import os
import shutil
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
import tempfile
from django.core.files.base import ContentFile

#-----------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
#os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#-------------------------------------------------------------------------------------------------------------
def extract_pdf_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    
    metadata = {
        "Title": doc.metadata.get("title", ""),
        "Authors": doc.metadata.get("authors", ""),
        "CreationDate": doc.metadata.get("creationDate", ""),
        "Subject": doc.metadata.get("subject", ""),
    }

    doc.close()
    
    return metadata
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
        num_pages (int): The number of pages to extract from the beginning and end.
    Returns:
        tuple: Three strings representing the full text, text of the first 5 pages, and text of the last 5 pages.
    """
    num_pages= 2
    
    # Open the PDF file using PyMuPDF's fitz module.
    pdf_file = fitz.open(file_path)

    full_text = ''  # Initialize an empty string to store the full text.
    first_pages_text = ''  # Initialize an empty string to store the text of the first 5 pages.
    last_pages_text = ''  # Initialize an empty string to store the text of the last 5 pages.

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
                    full_text += b[4] + '\n'
                    if page_num < num_pages:
                        first_pages_text += b[4] + '\n'
                    elif page_num >= pdf_file.page_count - num_pages:
                        last_pages_text += b[4] + '\n'
        else:
            # If only one column is present, extract text from the entire page.
            blocks = page.get_text("blocks")

            for b in blocks:
                # Concatenate the text in each block along with its formatting
                full_text += b[4] + '\n'
                if page_num < num_pages:
                    first_pages_text += b[4] + '\n'
                elif page_num >= pdf_file.page_count - num_pages:
                    last_pages_text += b[4] + '\n'

    pdf_file.close()  # Close the PDF file.
    #full_text = clean_text(full_text)
    #first_pages_text = clean_text(first_pages_text)
    #last_pages_text = clean_text(last_pages_text)

    return full_text, first_pages_text, last_pages_text
#--------------------------------------------------------------------------------
def extract_text_from_pdf_url(pdf_url):
    """
    Extract and organize text from a PDF URL considering multi-column layout.
    Parameters:
        pdf_url (str): The URL of the PDF file.
    Returns:
        tuple: Three strings representing the full text, text of the first 5 pages, and text of the last 5 pages.
    """
    num_pages = 3

    # Download the PDF content from the URL
    response = requests.get(pdf_url, stream=True)
    
    if response.status_code == 200:
        pdf_content = response.content
        pdf_file = fitz.open("pdf", pdf_content)

        full_text = ''  # Initialize an empty string to store the full text.
        first_pages_text = ''  # Initialize an empty string to store the text of the first 5 pages.
        last_pages_text = ''  # Initialize an empty string to store the text of the last 5 pages.

        # Iterate through each page in the PDF file.
        for page_num in range(pdf_file.page_count):
            page = pdf_file[page_num]  # Get the current page.

            # Use the column_boxes function to detect column bounding boxes.
            bboxes = fitz.Column(page, footer_margin=50, no_image_text=True).column_rects

            if bboxes:
                # If two columns are detected, extract text from each column separately.
                for rect in bboxes:
                    # Use "blocks" mode to preserve text formatting
                    blocks = page.get_text("blocks", clip=rect, sort=True)

                    for b in blocks:
                        # Concatenate the text in each block along with its formatting
                        full_text += b[4] + '\n'
                        if page_num < num_pages:
                            first_pages_text += b[4] + '\n'
                        elif page_num >= pdf_file.page_count - num_pages:
                            last_pages_text += b[4] + '\n'
            else:
                # If only one column is present, extract text from the entire page.
                blocks = page.get_text("blocks")

                for b in blocks:
                    # Concatenate the text in each block along with its formatting
                    full_text += b[4] + '\n'
                    if page_num < num_pages:
                        first_pages_text += b[4] + '\n'
                    elif page_num >= pdf_file.page_count - num_pages:
                        last_pages_text += b[4] + '\n'

        pdf_file.close()  # Close the PDF file.

        return full_text, first_pages_text, last_pages_text
    else:
        print(f"Failed to download PDF from the provided URL. Status code: {response.status_code}")
        return None, None, None
#--------------------------------------------------------------------------------------------------------------
def is_email(text):
    # A simple regex to check if the text looks like an email address
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return bool(re.match(email_pattern, text))

from dateutil import parser
#//////////////////////////
#    extract_article_info 
#//////////////////////////
def extract_article_info(text,first_pages, last_pages):
    
    
    #try:
        # Check if the required information is present in the metadata
        #title = meta_data.get('Title')
        #authors = meta_data.get('Authors')
        #abstract = meta_data.get('Subject')
        #date = meta_data.get('CreationDate')

        #print(title)

        # If any required information is missing in metadata, proceed with regular expression-based extraction
       # if any(value is None for value in [title, authors, abstract, date]):
    
    # Define regular expressions for each section
    title_pattern = re.compile(r'^\s*(.*?)\n\n', re.DOTALL)
    authors_pattern = re.compile(r'\b(.*?)\n(?:Dr|Prof|Mr|Mrs|Ms)\.?\s+(?:\w+\.?\s+)+\w+', re.DOTALL)
    ''' institutions_pattern = re.compile(
    r'(?:Affiliation|Address|Dept(?:artment)?|Department|School)\s*:\s*(.*?)(?:,|\.|$)|'
    r'\b(?:university|institute|laboratory|center|college|hospital|department|school|faculty)\b\s*(?:of|at|in)\s*(.*?)(?:,|\.|$)|'
    r'(?:Author )?[\w\s]+,\s*(.*?)(?:,|\.|$)',
    re.IGNORECASE
    )'''
    institutions_pattern = re.compile(r'\bDepartment\s+of\s+(.*?)\b\.', re.IGNORECASE)
    #abstract_pattern = re.compile(r'Abstract(.*?)(?:Keywords|Introduction|)', re.DOTALL)
    abstract_pattern = re.compile(
    r'\b(?:Abstract|Summary)\b(?:.*?)'
    r'(?:(?:\d|[A-Za-z]+\s+)[A-Za-z]+|$|'
    r'\b(?:Keywords|Introduction|\d+\s*\n)\b)',
    re.DOTALL | re.IGNORECASE
    )
    keywords_pattern =re.compile(
    r'(?i)Keywords\n\n\s(.*?)(?=\n\s*(?:ACM Reference Format:|Introduction)|$)',
    re.DOTALL)
    references_pattern = re.compile(r'(?i)(?:References|Bibliography)(.*?)(?=$|\Z)', re.DOTALL)

    date_pattern = re.compile(
    r'Published:\s+(?P<date>\d{1,2}\s+[A-Z][a-z]+\s+\d{4}|'
    r'[A-Z][a-z]+\s+\d{1,2}(?:–|-)\d{1,2},\s+\d{4})|'
    r"\d{4}-\d{2}-\d{2}|"
    r"\d{2}/\d{2}/\d{4}|"
    r"[A-Z][a-z]+\d{1,2}-(?:\d{2}-){2}\d{2}|"
    r"\d{1,2} [A-Z][a-z]+\s+\d{4}",
    re.DOTALL
)

           # Extract information using regular expressions
    title_match = title_pattern.search(first_pages)
    authors_match = authors_pattern.search(first_pages)
    institutions_match = institutions_pattern.search(first_pages)
    abstract_match = abstract_pattern.search(first_pages)
    keywords_match = keywords_pattern.search(first_pages)
    references_match = references_pattern.search(text)  # Extract references from the last pages
    date_match = date_pattern.search(first_pages)

    # Get the matched groups
    title = title_match.group(1).strip() if title_match else None
    authors = authors_match.group().strip() if authors_match else None
    institutions = institutions_match.group().strip() if institutions_match else None

    abstract = abstract_match.group().strip() if abstract_match else None
    keywords = keywords_match.group().strip() if keywords_match else None
    references_text = references_match.group().strip() if references_match else None
    date = date_match.group().strip() if date_match else None

    # Split references based on the pattern (digit followed by a dot)
    references = re.split(r'\b\d+\.', references_text) if references_text else []
    # Remove empty references (if any)
    references = [ref.strip() for ref in references if ref.strip()]

    #if not authors or not institutions:
    # If authors or institutions are not found using regex, use spaCy for entity recognition
           # Specify the number of lines to consider for entity recognition
    lines_for_entity_recognition = 40  # Adjust this based on the actual number of lines containing authors and institutions

    # Extract the relevant part of the text for entity recognition
    relevant_text = '\n'.join(first_pages.split('\n')[:lines_for_entity_recognition])

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(relevant_text)
    if not authors or not institutions:
        # Extract authors using spaCy
        authors_entities = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]

        # Eliminate duplicate authors and exclude emails
        #unique_authors = list(set(authors_entities))
        filtered_authors = [author for author in authors_entities if not is_email(author) and len(author) <= 40]

        # Convert the list of authors to a comma-separated string
        unique_authors = list(set(filtered_authors))
        authors = '| '.join(unique_authors) if unique_authors else None

    if not institutions:
        # Extract institution using spaCy
        institution_entities = [entity.text for entity in doc.ents if entity.label_ == "ORG" and not is_email(entity.text) and len(entity.text) >= 6]
        # Convert the list of authors to a comma-separated string
        unique_institution = list(set(institution_entities))
        institutions = '| '.join(unique_institution) if unique_institution else None
    '''
    if not date:
        # Extract entities using Spacy's named entity recognition
        date_entities = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

        # If no DATE entities are found, attempt to parse dates from the text
        if not date_entities:
           parsed_dates = [parser.parse(token.text, fuzzy=True) for token in doc if token.pos_ == "NUM"]
           date_entities = [date.strftime('%B %d, %Y') for date in parsed_dates]
    #except Exception as e:
        #print(f"Error: {e}")
        #return False
    # Return a dictionary with extracted information
    '''
    article_info = {
        'title': title,
        'authors': authors,
        'institutions': institutions,
        'abstract': abstract,
        'keywords': keywords,
        'references': references,
        'date': date
    }
    #print(title)
    #print(authors)
    #print(institutions)
    #print(abstract)
    print("key",keywords)
    #print(references)
    #print(date)



    return article_info

#------------------------------------------------------------------------------

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
    # Download PDF from the given URL
    response = requests.get(url)

    # Check if the response status code is 200 (HTTP OK)
    if response.status_code == 200:
        # Define the local file path to save the downloaded PDF
        local_file_path = '..\\articles_pdf\\downloaded_pdf.pdf'
        # Open the local file in binary write mode ('wb') and write the content of the response to it
        with open(local_file_path, 'wb') as file:
            file.write(response.content)

        # Return the local file path
        return local_file_path
        
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
        return None
    
#--------------------------------------------------------------------------------
def is_valid_scientific_pdf(file_path):
    """
    Check if the given PDF file meets the criteria for a scientific article.

    :param file_path: The path of the PDF file to be checked.
    :type file_path: str
    :return: True if the PDF is a valid scientific article, False otherwise.
    :rtype: bool
    """
    # Check if the file path is not None, is a local file, and has a valid extension
    if not (file_path and os.path.isfile(file_path) and file_path.lower().endswith('.pdf')):
        logging.debug(f"File {file_path} is not a PDF or has an invalid path.")
        return False

    # Check if there is at least one page
    with fitz.open(file_path) as pdf_document:
        if pdf_document.page_count < 1:
            logging.debug(f"PDF {file_path} has no pages.")
            return False

        # Extract text from all pages
        all_pages_text = ""
        for page_number in range(pdf_document.page_count):
            all_pages_text += pdf_document[page_number].get_text("text").lower()

    # Scientific article structure validation
    keywords_found = ["abstract", "introduction", "methods", "results", "conclusion", "keywords", "references", "bibliography"]
    if any(keyword in all_pages_text for keyword in keywords_found):
        logging.debug(f"Validation result for PDF {file_path}: True")
        return True
    else:
        logging.debug(f"PDF {file_path} does not contain scientific article keywords.")
        return False