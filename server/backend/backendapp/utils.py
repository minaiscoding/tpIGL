import os
import shutil
import requests
import logging
import validators
#--------------------------------------------------------------------------------------------------------------
# managing files
from urllib.parse import urlparse, unquote
import tempfile
from django.core.files.base import ContentFile
from dateutil import parser
from datetime import datetime, timedelta
#--------------------------------------------------------------------------------------------------------------
# extract info using python bib
from io import BytesIO
import spacy
from spacy.matcher import PhraseMatcher
import nltk
import re
from rake_nltk import Rake
#--------------------------------------------------------------------------------------------------------------
# manipulating pdfs
import PyPDF2
import fitz  # PyMuPDF
from pdfreader import PDFDocument
import pdfreader.viewer
import pdfminer
from bs4 import BeautifulSoup
#--------------------------------------------------------------------------------------------------------------
# for ocr
from PIL import Image
import pytesseract
#-----------------------------------------------------------------------------
from elasticsearch import Elasticsearch
#-----------------------------------------------------------------------------

#                               utils.py --> functions used in views

#----------------------------------------------------------------------------------------------------
# for config ocr
#os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#----------------------------------------------------------------------------------------------------
#///////////////////////
# extract_pdf_metadata 
#///////////////////////
def extract_pdf_metadata(file):
    """
    Extract metadata from a PDF file.

    :param str pdf_path: The path to the PDF file.
    
    :return: A dictionary containing the extracted metadata.
             Keys include 'Title', 'Authors', 'CreationDate', and 'Subject'.
    :rtype: dict
    """

    file_content = file.read()
    # Create a BytesIO object to wrap the file content
    pdf_bytes_io = BytesIO(file_content)

    # Open the PDF using fitz
    doc = fitz.open(stream=pdf_bytes_io)

    # Extract metadata information
    metadata = {
        "Title": doc.metadata.get("title", ""),
        "Authors": doc.metadata.get("authors", ""),
        "CreationDate": doc.metadata.get("creationDate", ""),
        "Abstract": doc.metadata.get("subject", ""),
        "Keywords": doc.metadata.get("keywords", ""),
    }

    # Close the PDF document
    doc.close()

    # Return the extracted metadata
    return metadata
#--------------------------------------------------------------------------------------------------------------
#///////////////////////
#    pdf_to_images 
#///////////////////////
def pdf_to_images(file):
    """
    Convert PDF pages to a list of images.

    :param str file_path: The path to the PDF file.

    :return: A list of PIL Image objects representing each page in the PDF.
    :rtype: list[Image.Image]
    """
    file_content = file.read()
    # Create a BytesIO object to wrap the file content
    pdf_bytes_io = BytesIO(file_content)

    # Open the PDF document using PyMuPDF (fitz)
    pdf_document = fitz.open(stream=pdf_bytes_io)
    

    # Initialize an empty list to store images
    images = []

    # Iterate through each page in the PDF
    for page_num in range(pdf_document.page_count):
        # Get the page object
        page = pdf_document[page_num]

        # Get the pixmap of the page
        image = page.get_pixmap()

        # Convert the pixmap to a PIL Image
        img = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Append the image to the list
        images.append(img)

    # Close the PDF document
    pdf_document.close()

    # Return the list of images
    return images

#--------------------------------------------------------------------------------------------------------------
#//////////////////////////////////////////
#  extract_text_with_ocr from pdf images
#//////////////////////////////////////////
def extract_text_with_ocr(images):
    """
    Extract text using OCR from a list of images.

    :param list images: A list of PIL Image objects.

    :return: The extracted text from the images.
    :rtype: str
    """
    # Initialize an empty string to store the extracted text
    extracted_text = ''

    # Iterate through each image in the list
    for image in images:
        # Perform OCR on the image using pytesseract
        text = pytesseract.image_to_string(image, lang='eng')

        # Add the extracted text to the overall text, with newlines between pages
        extracted_text += text + '\n'

        # Clean the extracted text (assuming a clean_text function is defined)
        extracted_text = clean_text(extracted_text)

    # Return the extracted text
    return extracted_text
#--------------------------------------------------------------------------------------------------------------
#///////////////////////
# column_boxes  
#///////////////////////
def column_boxes(page: fitz.Page, footer_margin: int = 0, no_image_text: bool = True) -> list:
    """
    Return a list of column bounding boxes for the given page.

    :param page: The PyMuPDF (fitz) page object.
    :type page: fitz.Page

    :param int footer_margin: The margin to exclude from the bottom of the page for detecting columns.
                             Default is 0.

    :param bool no_image_text: Flag to exclude text within images from column detection.
                               Default is True.

    :return: A list of bounding boxes representing columns on the page.
    :rtype: list
    """
#--------------------------------------------------------------------------------------------------------------
#////////////////////////////////
# clean_text Function
#////////////////////////////////
def clean_text(text):
    """
    Clean the extracted text by removing unwanted symbols, formatting,
    and lines matching specific patterns.

    :param str text: The text to be cleaned.

    :return: The cleaned text.
    :rtype: str
    """
    # Remove lines that match the specified image pattern or contain links or emails
    text_lines = text.split('\n')
    text_lines = [
        line for line in text_lines
        if not re.match(r'image: ICCBased\(RGB,sRGB v4 ICC preference perceptual intent beta\), width: \d+, height: \d+, bpc: \d+', line)
        and 'http' not in line  # Exclude lines containing 'http' (links)
        and 'www.' not in line  # Exclude lines containing 'http' (links)
        and '@' not in line  # Exclude lines containing '@' (emails)
        and 'bpc:' not in line  # Exclude lines containing 'bpc:' (images conf)
    ]

    # Join the remaining lines back into a single string
    text = '\n'.join(text_lines)

    # Remove special characters and symbols using regular expression
    cleaned_text = re.sub(r'\[^a-zA-Z0-9\s\.,;:() - –!?\]', '', text)

    return cleaned_text

#--------------------------------------------------------------------------------------------------------------
#////////////////////////////////
# extract_text_from_pdf Function
#////////////////////////////////
def extract_text_from_pdf(file, num_pages=2):
    """
    Extract and organize text from a PDF file considering multi-column layout.

    :param str file_path: The path to the PDF file.
    :param int num_pages: The number of pages to extract from the beginning and end. Default is 2.

    :return: Three strings representing the full text, text of the first `num_pages` pages, and text of the last `num_pages` pages.
    :rtype: tuple
    """
    # Read the content of the file
    file_content = file.read()
    
    # Check if the file content is not empty
    if not file_content:
       raise ValueError("File content is empty.")

    # Create a BytesIO object to wrap the file content

    pdf_bytes_io = BytesIO(file_content)

    # Open the PDF file using PyMuPDF's fitz module.
    pdf_file = fitz.open(stream=pdf_bytes_io) 

    # Determine the actual number of pages to extract based on the total number of pages in the PDF
    num_pages_to_extract = min(num_pages, pdf_file.page_count)

    # Initialize empty strings to store text
    full_text = ''         # to store the full text
    first_pages_text = ''  # to store the num_pages first pages
    last_pages_text = ''   # to store the num_pages last pages

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

                    if page_num < num_pages_to_extract:
                        first_pages_text += b[4] + '\n'
                    elif page_num >= pdf_file.page_count - num_pages_to_extract :
                        last_pages_text += b[4] + '\n'
        else:
            # If only one column is present, extract text from the entire page.
            blocks = page.get_text("blocks")

            for b in blocks:
                # Concatenate the text in each block along with its formatting
                full_text += b[4] + '\n'
                if page_num < num_pages_to_extract:
                    first_pages_text += b[4] + '\n'
                elif page_num >= pdf_file.page_count - num_pages_to_extract :
                    last_pages_text += b[4] + '\n'

    pdf_file.close()  # Close the PDF file.

    # clean the texts 
    full_text = clean_text(full_text)
    first_pages_text = clean_text(first_pages_text)
    last_pages_text = clean_text(last_pages_text)

    return full_text, first_pages_text, last_pages_text
#--------------------------------------------------------------------------------------------------------------
#////////////////////////////////
# download_pdf_from_url
#////////////////////////////////

#def download_pdf_from_url(url):
    """
    Download a PDF file from the given URL and return the file object.

    :param str url: The URL of the PDF file.

    :return: The file object containing the downloaded PDF content.
    :rtype: io.BytesIO
    """
#    try:
#       response = requests.get(url,stream=True)
#        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Create a BytesIO object to hold the PDF content
#        pdf_file = BytesIO(response.content)

#       return pdf_file
#    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions (e.g., network issues)
#        print(f"Error downloading PDF: {e}")
#        return None
    
def download_pdf_from_url(url):
    """
    Download a PDF file from a given URL and return the file object.
    """
    try:
        # Send a request to the URL
        response = requests.get(url,stream=True)
        response.raise_for_status()

        # Check if the content is HTML (indicating a redirection page)
        if 'text/html' in response.headers['Content-Type']:
            # Parse HTML to find the link to the actual PDF file
            soup = BeautifulSoup(response.content, 'html.parser')
            pdf_link = soup.find('a', {'href': lambda s: s and s.endswith('.pdf')})
            if pdf_link:
                pdf_url = pdf_link['href']
                pdf_response = requests.get(pdf_url)
                pdf_response.raise_for_status()

                pdf_file = BytesIO(pdf_response.content)

                return pdf_file
                #return pdf_response.content
            else:
                raise ValueError(f"No PDF link found on the page: {url}")

        # If the content is already a PDF, return it
        elif 'application/pdf' in response.headers['Content-Type']:

            return response.content

        else:
            raise ValueError(f"Unsupported content type: {response.headers['Content-Type']}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        return None
#--------------------------------------------------------------------------------------------------------------
#////////////////////////////////
# is_email
#////////////////////////////////
def is_email(text):
    """
    Check if the given text resembles an email address.

    :param str text: The text to be checked.

    :return: True if the text resembles an email address, False otherwise.
    :rtype: bool
    """
    # A simple regex to check if the text looks like an email address
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # Return True if the text matches the email pattern, otherwise False
    return bool(re.match(email_pattern, text))
#--------------------------------------------------------------------------------------------------------------
#//////////////////////////
#  extract_article_info 
#//////////////////////////
def extract_article_info(text, first_pages, last_pages):
    """
    Extract information from an article including title, authors, institutions, abstract, keywords, references, and date.

    :param str text: The full text of the article.
    :param str first_pages: Text from the first pages of the article.
    :param str last_pages: Text from the last pages of the article.

    :return: A dictionary containing extracted information.
    :rtype: dict
    """
    try:
        # Define regular expressions for each section
        title_pattern = re.compile(
              r'^\s*(.*?)\n\n',
              re.DOTALL  
            )
        #________________________________________________________________________________________________
        authors_pattern = re.compile(
              r'\b(.*?)\n(?:Dr|Prof|Mr|Mrs|Ms)\.?\s+(?:\w+\.?\s+)+\w+',
              re.DOTALL
            )
        #________________________________________________________________________________________________
        institutions_pattern = re.compile(
             r'\bDepartment\s+of\s+(.*?)\b\.',
             re.IGNORECASE
            )
        #________________________________________________________________________________________________
        abstract_pattern = re.compile(
             r'Abstract\s*\n(.*?)\s*\n(?:Keywords|Introduction|Categories and Subject Descriptors(.*?)\n|1\. Introduction\n|\d+\s*\n|CCS CONCEPTS\n|$)',
             re.DOTALL | re.IGNORECASE
            )
        #________________________________________________________________________________________________
        keywords_pattern = re.compile(
             #r'Keywords\s*([\w\s,]+)\n|Keywords:(.*?)\n\n|Keywords\s*\n(.*?)\s*\n(?:ACM Reference Format|Introduction|1\. Introduction\n)',
            #r'/bKeywords\s/b*([\w\s,]+)\n',
            # re.IGNORECASE | re.DOTALL
            r'\bKeywords\b\s*([\w\s,]+)\n|Keywords:(.*?)\n\n', re.IGNORECASE | re.DOTALL
            )
        #________________________________________________________________________________________________
        references_pattern = re.compile(
             r'(?i)(?:References|\d\.References|Bibliography)(.*?)(?=$|\Z)',
              re.DOTALL | re.IGNORECASE 
             #r'\b(?:References|Bibliography)\b.*?([\s\S]+?)(?=\b[A-Z]|$)',
             #re.IGNORECASE | re.DOTALL
            )
        #________________________________________________________________________________________________
        date_pattern = re.compile(
             r'Published:\s+(?P<date>\d{1,2}\s+[A-Z][a-z]+\s+\d{4}|'
             r'[A-Z][a-z]+\s+\d{1,2}(?:–|-)\d{1,2},\s+\d{4})|'
             r"\d{4}-\d{2}-\d{2}|"
             r"\d{2}/\d{2}/\d{4}|"
             r"[A-Z][a-z]+\d{1,2}-(?:\d{2}-){2}\d{2}|"
             r"\d{1,2} [A-Z][a-z]+\s+\d{4}",
             re.DOTALL
            )
        #-----------------------------------------------------------------------------------------
        # Extract information using regular expressions
        title_match = title_pattern.search(first_pages)
        authors_match = authors_pattern.search(first_pages)
        institutions_match = institutions_pattern.search(first_pages)
        abstract_match = abstract_pattern.search(first_pages)
        keywords_match = keywords_pattern.search(first_pages)
        references_match = references_pattern.search(last_pages) 
        date_match = date_pattern.search(first_pages)
        #-----------------------------------------------------------------------------------------
        # Get the matched groups
        title = title_match.group(1).strip() if title_match else None
        authors = authors_match.group().strip() if authors_match else None
        institutions = institutions_match.group().strip() if institutions_match else None  
        abstract = abstract_match.group().strip() if abstract_match else None
        keywords = keywords_match.group().strip() if keywords_match else None
        references_text = references_match.group().strip() if references_match else None
        date = date_match.group().strip() if date_match else None

        # Split references based on the pattern (digit followed by a dot)
        references = re.split(r'\b\[\d\]+\.|\b\[\d\]|\d\.', references_text) if references_text else []
        # Remove empty references (if any)
        references = [ref.strip() for ref in references if ref.strip()]

        references_string = '\n'.join(references)

        if not keywords:

            r = Rake()
            r.extract_keywords_from_text(first_pages)
            keywords_list = r.get_ranked_phrases()

            # Limit the number of keywords
            keywords = keywords_list[:5]

            cleaned_keywords = []
            for keyword in keywords:
            # Remove unwanted characters and digits
                cleaned_keyword = ' '.join(filter(lambda x: x.isalpha(), keyword.split()))
                cleaned_keywords.append(cleaned_keyword)

            keywords=cleaned_keywords

        # If authors or institutions are not found using regex, use spaCy for entity recognition
        if not authors or not institutions:
            # Specify the number of lines to consider for entity recognition
            lines_for_entity_recognition = 40

            # Extract the relevant part of the text for entity recognition
            relevant_text = '\n'.join(first_pages.split('\n')[:lines_for_entity_recognition])

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(relevant_text)

            # Extract authors using spaCy
            authors_entities = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]

            # Eliminate duplicate authors and exclude emails
            filtered_authors = [author for author in authors_entities if not is_email(author) and len(author) <= 40]
            # Convert the list of authors to a pipe-separated string
            authors = ', '.join(set(filtered_authors)) if filtered_authors else None

            # Extract institution using spaCy
            institution_entities = [entity.text for entity in doc.ents if entity.label_ == "ORG" and not is_email(entity.text) and len(entity.text) >= 6]
            # Convert the list of authors to a comma-separated string
            institutions = ', '.join(set(institution_entities)) if institution_entities else None

        # Return a dictionary with extracted information
        article_info = {
            'title': title,
            'authors': authors,
            'institutions': institutions,
            'abstract': abstract,
            'keywords': keywords,
            'references': references_string,
            'date': date
        }
        #print('title :',title)
        #print('authors :',authors)
        #print('institutions :',institutions)
        #print('abstract :',abstract)
        #print('keywords :',keywords)
        #print('references :',references)
        #print('date :',date)

        return article_info
    except Exception as e:
        print(f"Error: {e}")
        return None   
#------------------------------------------------------------------------------
#//////////////////////////
# is_valid_scientific_pdf
#//////////////////////////
def is_valid_scientific_pdf(file):
    """
    Check if the given PDF file meets the criteria for a scientific article.

    :param str file_path: The path of the PDF file to be checked.
    
    :return: True if the PDF is a valid scientific article, False otherwise.
    :rtype: bool
    """
    file_content = file.read()
    # Create a BytesIO object to wrap the file content
    pdf_bytes_io = BytesIO(file_content)

    # Open the PDF file using PyMuPDF's fitz module.
    pdf_file = fitz.open(stream=pdf_bytes_io) 

    # Check if there is at least one page
    if pdf_file.page_count < 1:
        logging.debug(f"PDF {file} has no pages.")
        return False

    # Extract text from all pages
    all_pages_text = ""
    for page_number in range(pdf_file.page_count):
        all_pages_text += pdf_file[page_number].get_text("text").lower()

    # Scientific article structure validation
    keywords_found = ["abstract", "ACM Reference Format","Categories and Subject Descriptors","Research paper", "methods","methodology", "results","CCS CONCEPTS", "keywords", "references", "bibliography"]
    if any(keyword in all_pages_text for keyword in keywords_found):
        logging.debug(f"Validation result for PDF: True")
        return True
    else:
        logging.debug(f"PDF does not contain scientific article keywords.")
        return False
#------------------------------------------------------------------------------
#//////////////////////////
# send_to_elasticsearch
#//////////////////////////
def send_to_elasticsearch(index_name, data):
    """
    Sends data to Elasticsearch.

    :param str index_name: The name of the index.
    :param str document_type: The type of the document.
    :param dict data: The data to be sent.
    """
    es = Elasticsearch(['http://localhost:9200'],  verify_certs=False)
    # Index the data in Elasticsearch
    for document in data:
        es.index(index=index_name, body=document)
    print("Successfully indexed dummy data.")
#------------------------------------------------------------------------------
#//////////////////////////
# parse_and_validate_date
#//////////////////////////
def parse_and_validate_date(date_string):
    try:
        # Parse the date string using the expected format
        parsed_date = datetime.strptime(date_string, '%d %b %Y')
        
        # Format the date into YYYY-MM-DD format
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        
        return formatted_date

    except ValueError:
        return None
#------------------------------------------------------------------------------
#//////////////////////////
# parse_metadata_date
#//////////////////////////   
def parse_metadata_date(date_string):
    try:
        # Extract date and time components
        date_time_str = date_string[2:14]
        timezone_offset_str = date_string[14:]

        # Convert timezone offset to hours and minutes
        hours = int(timezone_offset_str[:3])
        minutes = int(timezone_offset_str[3:])

        # Create a timedelta object for the timezone offset
        timezone_offset = timedelta(hours=hours, minutes=minutes)

        # Parse the date and time string
        parsed_date = datetime.strptime(date_time_str, '%Y%m%d%H%M%S')

        # Apply the timezone offset
        parsed_date -= timezone_offset

        # Return the parsed date in YYYY-MM-DD format
        return parsed_date.strftime('%Y-%m-%d')

    except ValueError:
        return None