import os
import requests
#--------------------------------------------------------------------------------------------------------------
from .utils import (
    extract_pdf_metadata,
    generate_metadata_dict,
    extract_text_from_pdf,
    extract_information,
    analyze_texte,
    is_valid_scientific_pdf,
    is_valid_external_url,
    is_valid_localfilepath,
    download_pdf_from_url,
    validate_articleSci_pdf,
)
#--------------------------------------------------------------------------------------------------------------
from django.core.files.base import ContentFile
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
#--------------------------------------------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
#--------------------------------------------------------------------------------------------------------------
from backendapp.models import Articles
from backendapp.serializers import  ArticlesSerializer
#--------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
#--------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------
#  for testing
#*****************************************************************************  

def pdf_text_view(request):
    file_path = "C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf"
    text = extract_text_from_pdf(file_path)
    return render(request, 'pdf_text.html', {'text': text})

#*****************************************************************************
def analize_text_view(request):
    
    file_path = "C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf"

    # Extract text from the PDF file
    pdf_text = extract_text_from_pdf(file_path)

    # Analyze the extracted text
    #result = extract_information(pdf_text)
    metadata = extract_pdf_metadata(file_path)
    result = analyze_texte(pdf_text,metadata)

    # Render the template with the extracted information
    return render(request, 'ana_text.html', {'result': result})
#*****************************************************************************
def pdf_metadata_view(request):
    # Extract metadata from the PDF file
    pdf_path = "C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf"
    metadata = extract_pdf_metadata(pdf_path)

    # Generate metadata dictionary
    metadata_dict = generate_metadata_dict(metadata)

    # Pass the metadata dictionary to the template
    return render(request, 'pdf_metadata_template.html', {'result': metadata_dict})


#*****************************************************************************
# to be tested by the end 
class UploadArticleView(APIView):
    parser_classes = (FileUploadParser, MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Retrieve the URL from the request data
        url = request.data.get('url')
        # If the URL points to a directory, download PDFs from the directory
        articles_data = download_pdf_from_url(url)

        if articles_data:
            for article_data in articles_data:
                # Save only the URL in the 'url' field
                url_field_data = {'url': url}
                article_data.update(url_field_data)

                # Serialize the data and create an Article instance
                serializer = ArticlesSerializer(data=article_data)

                if serializer.is_valid():
                    article = serializer.save()

                    # Extraire le texte du PDF et analyser les informations
                    pdf_text = extract_text_from_pdf(article.pdf_file.path)
                    analysis_result = analyze_texte(pdf_text)

        

                    article.save()

            return Response({'message': 'Upload réussi'}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Échec du téléchargement des PDFs depuis l\'URL'}, status=status.HTTP_400_BAD_REQUEST)

#///////////////////////////////////////////////////////////////////
from django.core.exceptions import ValidationError
class ArticleUploadViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    #parser_classes = (FileUploadParser, MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        pdf_file = request.data.get('pdf_File')

        if not url and not pdf_file:
            return Response({'error': 'A URL or a PDF file is required'}, status=status.HTTP_400_BAD_REQUEST)

        if url:
            # Handle URL upload
            articles_data = download_pdf_from_url(url)

            if articles_data:
                for article_data in articles_data:
                    url_field_data = {'URL_Pdf': url}
                    article_data.update(url_field_data)

                    serializer = self.get_serializer(data=article_data)
                    serializer.is_valid(raise_exception=True)
                    article = serializer.save()

                    pdf_text = extract_text_from_pdf(article.pdf_file)
                    analysis_result = analyze_texte(pdf_text)

                    article.save()

                headers = self.get_success_headers(serializer.data)
                return Response({'message': 'Upload réussi'}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({'error': 'Échec du téléchargement des PDFs depuis l\'URL'}, status=status.HTTP_400_BAD_REQUEST)

        elif pdf_file:
            # Handle local file upload
            if not pdf_file.content_type == 'application/pdf':
                return Response({'error': 'Only PDF files are allowed'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the file temporarily in the pdf_File field
            serializer = self.get_serializer(data={'pdf_File': pdf_file})
            try:
                serializer.is_valid(raise_exception=True)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            article = serializer.save()

            pdf_text = extract_text_from_pdf(article.pdf_file.path)
            analysis_result = analyze_texte(pdf_text)

            article.save()

            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'Upload réussi'}, status=status.HTTP_201_CREATED, headers=headers)

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

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backendapp.models import Articles
from backendapp.serializers import ArticlesSerializer
from .utils import download_pdf_from_url, extract_text_from_pdf, analyze_texte

#//////////////////////////////////
import PyPDF2
from io import BytesIO
#/////////////////////////////////
class LocalFileUploadView(APIView):

    def is_pdf(self, file_content):
        try:
            pdf_reader = PyPDF2.PdfFileReader(BytesIO(file_content))
            # Check if the file has at least one page to ensure it's a valid PDF
            return pdf_reader.numPages > 0
        except PyPDF2.utils.PdfReadError:
            return False
        
    def post(self, request, *args, **kwargs):
        print(request.data)
        local_file_path = request.data.get('local_file_path')

        if not local_file_path:
            return Response({'error': 'A file path is required'}, status=status.HTTP_400_BAD_REQUEST)

        if default_storage.exists(local_file_path):
            with default_storage.open(local_file_path, 'rb') as file:

                # Read the file content
                file_content = file.read()

                # Check if the file is a PDF
                if not self.is_pdf(file_content):
                    return Response({'error': 'Invalid file format. Only PDF files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

                #temp_file = NamedTemporaryFile(delete=True)
                #for chunk in file.chunks():
                #   temp_file.write(chunk)
                #temp_file.seek(0)

                #article_data = {'pdf_File': File(temp_file), 'URL_Pdf': local_file_path}
                #serializer = ArticlesSerializer(data=article_data)

                #try:
                #    serializer.is_valid(raise_exception=True)
                #except ValidationError as e:
                #    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                #article = serializer.save()
                # traitement
                #pdf_text = extract_text_from_pdf(article.URL_Pdf)
                #analysis_result = analyze_texte(pdf_text)

                return Response({'message': 'Upload pdf file successful'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'Invalid file path'}, status=status.HTTP_400_BAD_REQUEST)
#/////////////////////////////////
        
#/////////////////////////////////
class ExternalURLUploadView(APIView):
    def post(self, request, *args, **kwargs):
        url = request.data.get('url')

        if not url:
            return Response({'error': 'A URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        if url.startswith(('http://', 'https://')):
            articles_data = download_pdf_from_url(url)

            if articles_data:
                for article_data in articles_data:
                    url_field_data = {'URL_Pdf': url}
                    article_data.update(url_field_data)

                    serializer = ArticlesSerializer(data=article_data)

                    if serializer.is_valid():
                        article = serializer.save()
                        #traitement
                        #pdf_text = extract_text_from_pdf(article.URL_Pdf)
                        #analysis_result = analyze_texte(pdf_text)
                        article.save()

                return Response({'message': 'Upload successful'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to download PDFs from the URL'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Invalid URL format'}, status=status.HTTP_400_BAD_REQUEST)









#///////////////////////

#///////////////////////

def scientific_pdf_view(request):
    # Call the test_scientific_pdf function to get the validation result
    url='C:\\Users\\dell\\Downloads\\ScienceDirect_articles_14Dec2023_23-22-46.478\\An-Introduction-to-Machine-Learning--a-per_2023_Physica-A--Statistical-Mecha.pdf'
    url2='C:\\Users\\dell\\Downloads\\Artificial_Intelligence_Enabled_Radio_Propagation_for_CommunicationsPart_I_Channel_Characterization_and_Antenna-Channel_Optimization.pdf'
    is_valid = validate_articleSci_pdf(url2)

    # Prepare the context data to pass to the template
    context = {'is_valid': is_valid}

    # Render the template with the context data
    return render(request, 'test_scientific_pdf.html', context)

