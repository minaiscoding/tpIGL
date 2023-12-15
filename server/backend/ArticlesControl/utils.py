import requests
import logging
#--------------------------------------------------------------------------------------------------------------
import PyPDF2
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
#from PyMuPDF import FitReader
#--------------------------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from urllib.parse import urljoin
#--------------------------------------------------------------------------------------------------------------
import spacy
from io import BytesIO
#--------------------------------------------------------------------------------------------------------------
import re
import os
import validators


#--------------------------------------------------------------------------------------------------------------

''' tested successfully '''
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#//////////////////////////
#  is_valid_localfilepath
#//////////////////////////

def is_valid_localfilepath(file_path):
    """
    Check if the given file path is a valid local PDF file with a valid extension.

    :param file_path: The path of the file to be checked.
    :type file_path: str
    :return: True if the file path is a valid local PDF file, False otherwise.
    :rtype: bool
    """
    # Check if the file path is not None, is a local file, and has a valid extension
    if not (file_path and os.path.isfile(file_path) and file_path.lower().endswith('.pdf')):
        return False

    # Check the PDF file's magic number
    with open(file_path, 'rb') as file:
        magic_number = file.read(4).decode()
        if magic_number != "%PDF-":
            return False

    return True

#///////////////////////
# is_valid_external_url
#///////////////////////

def is_valid_external_url(url):
    """
    Check if the given URL is a valid URL with a valid protocol (http or https).

    :param url: The URL to be checked.
    :type url: str
    :return: True if the URL is valid and from a known source, False otherwise.
    :rtype: bool
    """
    # Check if the URL has a valid protocol (http or https)
    if not (url and (url.lower().startswith('http://') or url.lower().startswith('https://'))):
        return False

    # Check if the URL is a valid URL using the validators library
    if not validators.url(url):
        return False

    # Additional checks for known sources can be added here if needed

    return True


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

#///////////////////////////
#   validate_articleSci_pdf
#///////////////////////////
def validate_articleSci_pdf(request) -> bool:
    """
    Validate a PDF provided through either a local file path or an external URL.

    :param request: The Django request object.
    :return: True if the PDF is valid, False otherwise.
    :rtype: bool
    """
    # Extract file path from the request
    local_file_path = request
    # Initialize the validation status
    is_valid = False

    # Check if the provided file path is a valid local file
    if is_valid_localfilepath(local_file_path):
        is_valid = is_valid_scientific_pdf(local_file_path)
    
    # Check if the provided file path is a valid external URL
    elif is_valid_external_url(local_file_path):
        # Download the file and validate it
        downloaded_file_path = download_pdf_from_url(local_file_path)
        if downloaded_file_path:
            is_valid = is_valid_scientific_pdf(downloaded_file_path)
            os.remove(downloaded_file_path)
        else:
            # Download failed, return False
            return False
    else:
        # Invalid file path or URL, return False
        return False

    # Return the validation status
    return is_valid

#/////////////////////////
# is_valid_scientific_pdf
#/////////////////////////
# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the desired logging level

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
    '''
    # Check the PDF file's magic number
    with open(file_path, 'rb') as file:
        magic_number = file.read(4).decode()
        if magic_number != "%PDF-":
            logging.debug(f"File {file_path} does not have a valid PDF magic number.")
            return False
    '''
    # Check the first five pages for column count
    with fitz.open(file_path) as pdf_document:
        for page_number in range(min(3, pdf_document.page_count)):
            page = pdf_document[page_number]
            columns = page.getPageLayout().columns
            if columns > 2:
                logging.debug(f"PDF {file_path} has more than 2 columns on page {page_number + 1}.")
                return False

    # Basic PDF verification and text extraction
    try:
        pdf_document = fitz.open(file_path)
        if pdf_document.page_count < 3:  # Check if there are at least 3 pages
           logging.debug(f"PDF {file_path} has less than 3 pages.")
           return False

        # Extract text from the first three pages
        first_three_pages_text = ""
        for page_number in range(3):
            first_three_pages_text += pdf_document[page_number].get_text("text").lower()

    except Exception as e:
        logging.exception(f"Error while processing PDF {file_path}: {e}")
        return False

    # Scientific article structure validation
    nlp = spacy.load("en_core_web_sm")

    # Keyword and pattern checks
    keywords_found = ["Abstract", "Introduction", "methods", "results", "Conclusion", "Keywords"]
    keyword_count = sum(keyword in first_three_pages_text for keyword in keywords_found)
    '''pattern_matches = sum(
       bool(re.search(pattern, first_three_pages_text))
       for pattern in [r"\([1-9]\)", r"\(Author, year\)", r"\$\S+\$"]
      )    
    '''
    # NER and language
    #doc = nlp(first_three_pages_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    ##has_scientific_entities = any(label in ("ORG", "LOC", "PERSON") for text, label in entities)
    #language_detected = doc.lang_
    #is_english = language_detected == "en"

    # Threshold for validation
    minimum_keywords = 2
    minimum_patterns = 1

    result = (
        keyword_count >= minimum_keywords
        #and pattern_matches >= minimum_patterns
        #and has_scientific_entities
       # and is_english
    )

    logging.debug(f"Validation result for PDF {file_path}: {result}")
    return result


#///////////////////////
# column_boxes Function 
#///////////////////////

def column_boxes(page: fitz.Page, footer_margin: int = 0, no_image_text: bool = True) -> list:
    """Return list of column bounding boxes for the given page."""
    # Function to identify column bounding boxes on a page.
#     Uses the multi_column.column_boxes method from the 'multi_column' module.
#     Parameters:
#       - page: A fitz.Page object representing the PDF page.
#       - footer_margin: An integer specifying the margin from the bottom of the page (default: 0).
#       - no_image_text: A boolean indicating whether to include text in image regions (default: True).
#     Returns:
#     A list of column bounding boxes for the given page.

#////////////////////////////////
# extract_text_from_pdf Function
#////////////////////////////////
def extract_text_from_pdf(file_path):
    """Extract text from a PDF file considering multi-column layout.

    Parameters:
        file_path (str): The path to the PDF file.

    Returns:
        str: Extracted text.
    """
    # Implementation details:
    # - Opens the PDF file using PyMuPDF's fitz module.
    # - Iterates through each page in the PDF file.
    # - Uses the column_boxes function to detect column bounding boxes.
    # - Extracts text, considering one or two columns.
    # - Closes the PDF file and returns the extracted text.


    # Open the PDF file using PyMuPDF's fitz module.
    pdf_file = fitz.open(file_path)
    text = ''  # Initialize an empty string to store the extracted text.

     # Iterate through each page in the PDF file.
    for page_num in range(1,pdf_file.page_count):
        page = pdf_file[page_num] # Get the current page.
        
        # Use the column_boxes function to detect column bounding boxes.
        bboxes = column_boxes(page, footer_margin=50, no_image_text=True)

        if bboxes:
            # If two columns are detected, extract text from each column separately.
            column_text = []
            for rect in bboxes:
                column_text.append(page.get_text(clip=rect, sort=True))
            text += '\n'.join(column_text) # Combine text from both columns with newline separation.
        else:
            # If only one column is present, extract text from the entire page.
            text += page.get_text()

    pdf_file.close() # Close the PDF file.
    return text # Return the extracted text.



#///////////////////////

#///////////////////////
#to be tested 


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# to be tested 
#///////////////////////

#///////////////////////
def analyze_text(text):

    # Define regular expressions for extracting information
    title_pattern = re.compile(r'^\d+\s*(.*?)\n', re.DOTALL)
    institutions_pattern = re.compile(r'\n', re.DOTALL)
    abstract_pattern = re.compile(r'Abstract(.*?)Keywords', re.DOTALL)
    keywords_pattern = re.compile(r'Keywords(.*?)Introduction', re.DOTALL)
    abstract_pattern = re.compile(r'Abstract(.*?)Keywords', re.DOTALL)
    references_pattern = re.compile(r'References (.*?) ', re.DOTALL)
    date_pattern = re.compile(r'on(.*?)', re.DOTALL)

    # Extract information using regular expressions
    title_match = title_pattern.search(text)
    institutions_match = institutions_pattern.search(text)
    abstract_match = abstract_pattern.search(text)
    keywords_match = keywords_pattern.search(text)
    references_match = references_pattern.search(text)
    date_match = date_pattern.search(text)


    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    
    # Extracted information from regular expressions
    title = title_match.group(1).strip() if title_match else ""

    # Extract authors using spaCy
    authors_entities = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]
    authors = ', '.join(authors_entities) if authors_entities else None

    institutions = institutions_pattern.search(text).group().strip() if institutions_match else ""
    if not institutions :
        # Extract institution using spaCy
        institution_entities = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        institutions = ', '.join(institution_entities) if institution_entities else None

    abstract = abstract_match.group(1).strip() if abstract_match else ""
    keywords = keywords_match.group(1).strip() if keywords_match else ""
    references = references_pattern.search(text).group().strip() if references_match else ""
    date = date_match.group(1).strip() if date_match else ""

    return {
        "Title": title,
        "Authors": authors,
        "Institutions": institutions,
        "Abstract": abstract,
        "Keywords": keywords,
        "References": references,
        "Date": date
    }





#///////////////////////

#///////////////////////
def generate_metadata_dict(metadata):
    metadata_dict = {
        "Title": metadata.get("Title", ""),
        "Authors": metadata.get("Author", ""),
        "Institution": metadata.get("Institution", ""),
        "Abstract": metadata.get("Abstract", ""),
        "Keywords": metadata.get("Keywords", ""),
        "References": metadata.get("References", ""),
        "Date": metadata.get("Date", "")
    }
    return metadata_dict

#///////////////////////

#///////////////////////

def extract_pdf_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    
    metadata = {
        "Title": doc.metadata.get("title", ""),
        "Author": doc.metadata.get("author", ""),
        "Keywords": doc.metadata.get("keywords", ""),
        "Author": doc.metadata.get("author", ""),
        "Date": doc.metadata.get("date", ""),
    }

    doc.close()
    
    return metadata
#///////////////////////

#///////////////////////

def extract_information(text):
    # Define regular expressions for extracting information
    title_pattern = re.compile(r'^\d+\s*(.*?)\n', re.DOTALL)
    institutions_pattern = re.compile(r'\n', re.DOTALL)
    abstract_pattern = re.compile(r'Abstract(.*?)Keywords', re.DOTALL)
    keywords_pattern = re.compile(r'Keywords(.*?)Introduction', re.DOTALL)
    abstract_pattern = re.compile(r'Abstract(.*?)Keywords', re.DOTALL)
    references_pattern = re.compile(r'References (.*?) ', re.DOTALL)
    date_pattern = re.compile(r'on(.*?)', re.DOTALL)

    # Extract information using regular expressions
    title_match = title_pattern.search(text)
    institutions_match = institutions_pattern.search(text)
    abstract_match = abstract_pattern.search(text)
    keywords_match = keywords_pattern.search(text)
    references_match = references_pattern.search(text)
    date_match = date_pattern.search(text)

    # Extracted information
    title = title_match.group().strip() if title_match else None
    authors = title_match.group().strip() if title_match else None
    institutions = institutions_match.group().strip() if institutions_match else None
    abstract = abstract_match.group().strip() if abstract_match else None
    keywords = keywords_match.group().strip() if keywords_match else None
    references = references_match.group().strip() if references_match else None
    date = date_match.group().strip() if date_match else None

    if not authors or not institutions:
        # If authors or institutions are not found using regex, use spaCy for entity recognition
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        # Extract authors using spaCy
        authors_entities = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]
        authors = ', '.join(authors_entities) if authors_entities else None

        # Extract institution using spaCy
        institution_entities = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        institutions = ', '.join(institution_entities) if institution_entities else None

    # You may add more conditions or logic based on your specific requirements

    return {
        "Title": title,
        "Authors": authors,
        "Institutions": institutions,
        "Abstract": abstract,
        "Keywords": keywords,
        "References": references,
        "Date": date
    }


#///////////////////////

#///////////////////////
def analyze_texte(text,metadata):

    # Check if metadata contains information, use it if available
    title = metadata.get("Title", "")
    authors = metadata.get("Author", "")
    abstract = metadata.get("Abstract", "")
    keywords = metadata.get("Keywords", "")
    references = metadata.get("References", "")
    date = metadata.get("Date", "")
    #*********************************************************
    if not title:
       title_pattern = re.compile(r'^\d+\s*(.*?)\n', re.DOTALL)
       title_match = title_pattern.search(text)
       title = title_match.group(1).strip() if title_match else ""
    #*********************************************************   
    if not authors:
       nlp = spacy.load("en_core_web_sm")
       doc = nlp(text)
       # Extract authors using spaCy
       authors = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]
    #*********************************************************
    institutions_pattern = re.compile(r'\n', re.DOTALL)
    institutions_match = institutions_pattern.search(text)
    institutions = institutions_pattern.search(text).group().strip() if institutions_match else ""
    if not institutions:
        # Extract institution using spaCy
        institution_entities = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        institutions = ', '.join(institution_entities) if institution_entities else None
    #********************************************************* 
    if not abstract:
        abstract_pattern = re.compile(r'Abstract(.*?)Keywords', re.DOTALL)
        abstract_match = abstract_pattern.search(text)
        abstract = abstract_match.group(1).strip() if abstract_match else ""
    #*********************************************************
    if not keywords:
        keywords_pattern = re.compile(r'Keywords(.*?)Introduction', re.DOTALL)
        keywords_match = keywords_pattern.search(text)
        keywords = keywords_match.group(1).strip() if keywords_match else ""
    #*********************************************************
    if not references:
        references_pattern = re.compile(r'^References(.*?)', re.DOTALL)
        references_match = references_pattern.search(text)
        references = references_pattern.search(text).group().strip() if references_match else ""
    #*********************************************************
    if not date:
        date_pattern = re.compile(r'on(.*?)', re.DOTALL)
        date_match = date_pattern.search(text)
        date = date_match.group(1).strip() if date_match else ""
    #*********************************************************
    return {
        "Title": title,
        "Authors": authors,
        "Institutions": institutions,
        "Abstract": abstract,
        "Keywords": keywords,
        "References": references,
        "Date": date
    }

#/////////////////////////

#/////////////////////////


'''
def is_valid_scientific_pdf(file_path):
    # Enhanced file type check
    with open(file_path, 'rb') as file:
        magic_number = file.read(4).decode()
        if magic_number != "%PDF-":
            return False

    # Basic PDF verification
    try:
        pdf_reader = PyPDF2.PdfFileReader(file_path)
        if pdf_reader.numPages < 1:
            return False
    except PyPDF2.utils.PdfReadError:
        return False

    # Scientific article structure validation
    nlp = spacy.load("en_core_web_sm")
    first_page_text = pdf_reader.getPage(0).extractText().lower()

    # Keyword and pattern checks
    keywords_found = ["abstract", "introduction", "methods", "results", "conclusion"]
    keyword_count = sum(keyword in first_page_text for keyword in keywords_found)
    pattern_matches = sum(
        bool(re.search(pattern, first_page_text))
        for pattern in [r"\([1-9]\)", r"\(Author, year\)", r"\$\S+\$"]
    )

    # NER and language
    doc = nlp(first_page_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    has_scientific_entities = any(
        label in ("ORG", "LOC", "PERSON") for text, label in entities
    )
    language_detected = nlp(first_page_text).lang
    is_english = language_detected == "en"

    # Threshold for validation
    minimum_keywords = 3
    minimum_patterns = 2

    return (
        keyword_count >= minimum_keywords
        and pattern_matches >= minimum_patterns
        and has_scientific_entities
        and is_english
    )'''