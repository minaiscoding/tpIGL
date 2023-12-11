import requests
#--------------------------------------------------------------------------------------------------------------
import PyPDF2
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
#--------------------------------------------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
#--------------------------------------------------------------------------------------------------------------
from backendapp.models import Utilisateurs, Articles, Favoris
from backendapp.serializers import UtilisateursSerializer, ArticlesSerializer, FavorisSerializer
#--------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
#--------------------------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from urllib.parse import urljoin
#--------------------------------------------------------------------------------------------------------------
import spacy
#--------------------------------------------------------------------------------------------------------------

                                   #**************************#
                                   #     GestionArticles      #
                                   #**************************#

#////////////////
# upload article
#////////////////

#///////////////////////////////////////////////////////////////////
'''
Lancer une opération d Upload des articles scientifiques à partir d une adresse URL contenant un ensemble 
d articles en format PDF, ces articles peuvent être en une colonne ou deux colonnes maximum. Le système 
récupère les fichiers PDF, il extrait le texte, il analyse ces textes pour extraire les informations caractérisant 
l article scientifique. Les informations extraites sont envoyées dans un index de recherche dans ElasticSearch.
'''
#///////////////////////////////////////////////////////////////////


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#to be tested 
def download_pdfs_from_one_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = soup.find_all('a', href=lambda href: (href and href.endswith('.pdf')))

        articles = []
        for link in pdf_links:
            pdf_url = urljoin(url, link['href'])
            pdf_content = requests.get(pdf_url).content
            
            # Actuellement, cela renvoie simplement l'URL et le contenu du PDF pour illustration
            articles.append({'url': pdf_url, 'content': pdf_content})

        return articles

    return None



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# to be tested 

def analyze_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Exemple : Extraire les entités nommées (auteurs, lieux, organisations, etc.)
    authors = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]

    # Autres traitements spécifiques en fonction de ce que vous souhaitez extraire
    # Par exemple, extraire la première phrase pour le résumé
    sentences = list(doc.sents)
    summary = str(sentences[0]) if sentences else ''

    # Vous devez adapter ces extraits à la structure spécifique de votre modèle Articles
    return {
        'Titre': doc._.meta['title'],  # Supposons que le titre est stocké dans les métadonnées
        'Resume': summary,
        'auteurs': ', '.join(authors),
        'Institution': '...',  
        'date': '...',  
        'MotsCles': '...',  
        'text': text,
        'URL_Pdf': '...',  
        'RefBib': '...',  
    }

''' tested successfully '''
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#////////////////////////////////////////////////////////////////////
# column_boxes Function 
#////////////////////////////////////////////////////////////////////
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

#////////////////////////////////////////////////////////////////////
# extract_text_from_pdf Function
#////////////////////////////////////////////////////////////////////
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
#///////////////////////////////////////////////////////////////////

    # Open the PDF file using PyMuPDF's fitz module.
    pdf_file = fitz.open(file_path)
    text = ''  # Initialize an empty string to store the extracted text.

     # Iterate through each page in the PDF file.
    for page_num in range(pdf_file.page_count):
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

#///////////////////////////////////////////////////////////////////
#  for testing
'''  
def pdf_text_view(request):
    file_path = "C:\\Users\\dell\\Downloads\\New_Fac_101.pdf"
    text = extract_text_from_pdf(file_path)
    return render(request, 'pdf_text.html', {'text': text})
'''
#///////////////////////////////////////////////////////////////////

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# to be tested by the end 
class UploadArticleView(APIView):
    #parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Télécharger les PDFs à partir de l'URL
        url = request.data.get('url')
        articles_data = download_pdfs_from_one_url(url)

        if articles_data:
            # Créer des instances Articles avec les informations téléchargées
            for article_data in articles_data:
                serializer = ArticlesSerializer(data=article_data)

                if serializer.is_valid():
                    article = serializer.save()

                    # Extraire le texte du PDF et analyser les informations
                    pdf_text = extract_text_from_pdf(article.pdf_file.path)
                    analysis_result = analyze_text(pdf_text)

                    # Mettre à jour l'instance de l'article avec les informations analysées
                    for key, value in analysis_result.items():
                        setattr(article, key, value)

                    article.save()

            return Response({'message': 'Upload réussi'}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Échec du téléchargement des PDFs depuis l\'URL'}, status=status.HTTP_400_BAD_REQUEST)

#///////////////////////////////////////////////////////////////////
# other version to review 
'''
class UploadArticleView(APIView):
     parser_classes = (MultiPartParser, FormParser)
     def post(self, request, *args, **kwargs):

        serializer = ArticlesSerializer(data=request.data)
        if serializer.is_valid():
           # Enregistrez le fichier PDF dans la base de données
           article = serializer.save()
           # Extract information from the uploaded PDF
           pdf_text = extract_text_from_pdf(article.pdf_file.path)

            # Analyser le texte et extraire les informations nécessaires
            # Vous devez implémenter la logique d'analyse en fonction de vos besoins
           return Response({'message': 'Upload réussi'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
           article_data = {
                    'Titre': ,
                    'Resume': ,
                    'auteurs': ,
                    'Institution': ,
                    'date': ,
                    'MotsCles': ,
                    'text': ,
                    'URL_Pdf': ,
                    'RefBib': ,
                }
           # Create a new article instance with the extracted information
           Articles.objects.create(**article_data)
           '''
'''
#--------------------------------------------------------------

'''
'''
def extract_text_from_file(article_file:str) -> [str]:
    with open(article_file,'rb') as pdf:
        reader = PyPDF2.PdfFileReader(pdf,strict=False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
    

class UploadArticleView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ArticlesSerializer(data=request.data)

        if serializer.is_valid():
            # Extract information from the uploaded PDF
            article_file = request.FILES['article_file']

            try:
                # Open the PDF file using PyMuPDF
                pdf_document = fitz.open(article_file)
                
                # Assuming you want to extract text from the first page
                first_page = pdf_document[0]
                extracted_text = first_page.get_text("text")

                # Extracted information from the PDF

                # Modify this part based on your actual extraction logic
                extracted_title = "Title from PDF"
                extracted_resume = "Resume from PDF"
                extracted_authors = "Authors from PDF"
                extracted_institution = "Institution from PDF"
                extracted_date = "Date from PDF"
                extracted_mots_cles = "MotsCles from PDF"
                extracted_text = first_page.get_text("text")
                extracted_url_pdf = "URL_Pdf from PDF"
                extracted_ref_bib = "RefBib from PDF"

                # Create a new article instance with the extracted information
                article_data = {
                    'Titre': extracted_title,
                    'Resume': extracted_resume,
                    'auteurs': extracted_authors,
                    'Institution': extracted_institution,
                    'date': extracted_date,
                    'MotsCles': extracted_mots_cles,
                    'text': extracted_text,
                    'URL_Pdf': extracted_url_pdf,
                    'RefBib': extracted_ref_bib,
                }

                Articles.objects.create(**article_data)

                return Response({'message': 'Article uploaded and information extracted.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                pdf_document.close()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''