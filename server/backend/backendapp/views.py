import uuid
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.core.files.storage import default_storage
#--------------------------------------------------------------------------------
from .models import Utilisateurs, Articles, Favoris
from .serializers import UtilisateursSerializer, ArticlesSerializer, FavorisSerializer
#--------------------------------------------------------------------------------
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import action,api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
#--------------------------------------------------------------------------------
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
import json
import requests
import PyPDF2
import nltk
import os
#--------------------------------------------------------------------------------
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
#------------------------------------------------------------------
from .utils import (  extract_text_from_pdf,
                      download_pdf_from_url,
                      pdf_to_images,
                      parse_metadata_date,
                      extract_pdf_metadata,
                      extract_text_with_ocr,
                      parse_and_validate_date,
                      is_valid_scientific_pdf,
                      extract_article_info, 
                      download_pdf_from_url, 
                      send_to_elasticsearch,            
                   )
#--------------------------------------------------------------------------------------------------------------

#                               views.py --> api endpoints

#--------------------------------------------------------------------------------------------------------------

class UtilisateursListView(generics.ListAPIView):
    queryset = Utilisateurs.objects.all()
    serializer_class = UtilisateursSerializer

class ArticlesListView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Perform the Elasticsearch search to get all articles
        search = Search(index='articles').query('match_all')
        response = search.execute()

        # Extract relevant information from search hits
        hits = [{'id': hit.meta.id, **hit.to_dict()} for hit in response.hits]
        

        # Serialize the search results using your existing serializer
        serializer = ArticlesSerializer(data=hits, many=True)
        serializer.is_valid()

        # Return the serialized results as JSON
        return Response(serializer.data)


class FavorisListView(generics.ListAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer



class SearchView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Get the search query from the request parameters
        query = request.GET.get('q', '')

        # Get start and end dates from the request parameters
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        # Get the selected filter type from the request parameters
        filter_type = request.GET.get('filter_type', 'Titre')

        # Initialize the date range filter as an empty list
        date_range_filter = []

        # Check if start_date and end_date are not empty before including them in the filter
        if start_date and end_date:
            date_range_filter = [{'range': {'date': {'gte': start_date, 'lte': end_date}}}]

        # Perform the Elasticsearch search with dynamic query and date range filter
        search = Search(index='articles').query('bool', filter=date_range_filter).query('match', **{filter_type: query})

        try:
            response = search.execute()

            # Extract relevant information from search hits
            hits = [{'id': hit.meta.id, **hit.to_dict()} for hit in response.hits]

            # Serialize the search results using your existing serializer
            serializer = ArticlesSerializer(data=hits, many=True)
            serializer.is_valid()

        except Exception as e:
            # Handle exceptions, log them, or return an appropriate error response
            return JsonResponse({'error': str(e)}, status=500)

        # Return the serialized results as JSON            
        return Response(serializer.data)
    
#///////////////////////////////////////////////////////////////////
'''
Lancer une opération d Upload des articles scientifiques à partir d une adresse URL contenant un ensemble 
d articles en format PDF, ces articles peuvent être en une colonne ou deux colonnes maximum. Le système 
récupère les fichiers PDF, il extrait le texte, il analyse ces textes pour extraire les informations caractérisant 
l article scientifique. Les informations extraites sont envoyées dans un index de recherche dans ElasticSearch.
'''
#///////////////////////////////////////////////////////////////////

#--------------------------------------------------------------------------------------------------------------#  
 
    #------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #-------------------------#
    #------------------------------------------------------------------------#
article_test = "01"
#--------------------------------------------------------------------------------------------------------------#
#///////////////////////
# pdf_metadata_view
#///////////////////////
def pdf_metadata_view(request):
    # Assuming you have the article_test variable defined

    # Extract metadata from the PDF file
    pdf_file_path = f"C:\\Users\\dell\\Downloads\\Articles\\EchantillonsArticles\\Article_"+article_test+".pdf"
    with open(pdf_file_path, 'rb') as file:
        metadata = extract_pdf_metadata(file)
        
        date_str = metadata.get("CreationDate", "")

        date_meta = parse_metadata_date(date_str)
        # Generate metadata dictionary
        metadata_dict = {
        # Extracted PDF metadata keys
        "Title": metadata.get("Title", ""),
        "Authors": metadata.get("Author", ""),  
        "Keywords": metadata.get("Subject", ""),
        "Date": date_meta
        }

    # Pass the metadata dictionary to the template
    return render(request, 'pdf_metadata_template.html', {'result': metadata_dict})
#--------------------------------------------------------------------------------------------------------------#
#///////////////////////
# scientific_pdf_view
#///////////////////////

def scientific_pdf_view(request):
    """
    View function to check if a given PDF file meets the criteria for a scientific article.

    :param HttpRequest request: The request object.

    :return: Rendered template with the validation result.
    """
    # Provide the path to the PDF file to be checked
    # In a real-world scenario, this could be obtained from the user input or other sources
    pdf_file_path = "C:\\Users\\dell\\Downloads\\Articles\\EchantillonsArticles\\Article_"+article_test+".pdf"
    with open(pdf_file_path, 'rb') as file:
       # Call the is_valid_scientific_pdf function to get the validation result
       is_valid = is_valid_scientific_pdf(file)

    # Render the template with the context data
    return render(request, 'test_scientific_pdf.html', {'is_valid': is_valid})
#--------------------------------------------------------------------------------------------------------------#
#/////////////////////////////////////////////////
#    pdf_text_view 
#/////////////////////////////////////////////////
def pdf_text_view(request):
    """
    View function to display the extracted text from a PDF file.

    :param HttpRequest request: The request object.

    :return: Rendered template with the extracted text.
    """
    # Provide the path to the PDF file to be processed
    #url ="https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9721302"
    #if url:
    pdf_file_path = "C:\\Users\\dell\\Downloads\\Articles\\EchantillonsArticles\\Article_"+article_test+".pdf"

# ******************* way 1 ***********************
    # Extract text from the PDF file
    with open(pdf_file_path, 'rb') as file:
        full_text, first_pages_text, last_pages_text = extract_text_from_pdf(file) 
# ******************* way 2 **********************
    # convert pdf pages into images 
    # pdf_images = pdf_to_images(file_path)
    # Extract text using OCR from the pdf's images --> process takes a lot of time it's not recommended
    #extracted_text = extract_text_with_ocr(pdf_images)

    # Render the template with the context data

    return render(request, 'pdf_text.html', {'full_text': full_text, 'first_pages': first_pages_text, 'last_pages': last_pages_text})

#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#   analize_text_view to view the extracted info of the article  
#//////////////////////////////////////////////////////////////
def analize_text_view(request):
    """
    View function to analyze the text extracted from a PDF file.

    :param HttpRequest request: The request object.

    :return: Rendered template with the analysis result.
    """
    

    #url ="https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9721302"
    #if url:

    # Provide the path to the PDF file to be processed
    pdf_file_path = "C:\\Users\\dell\\Downloads\\Articles\\EchantillonsArticles\\Article_"+article_test+".pdf"
    
# ***************** way 1 ********************
    # Extract text from the PDF file
    with open(pdf_file_path, 'rb') as file:
        # Extract text from the PDF file
        pdf_text, first_pages_text, last_pages_text = extract_text_from_pdf(file)

        # Analyze the extracted text
        result = extract_article_info(pdf_text, first_pages_text, last_pages_text)

#  *************** way 2 ********************
    # convert pdf pages into images 
    #pdf_images = pdf_to_images(file_path)
    # Extract text using OCR from the pdf's images --> process takes a lot of time it's not recommended
    #pdf_text = extract_text_with_ocr(pdf_images)
    # Analyze the extracted text
    #result = extract_article_info(pdf_text)
    

    # Render the template with the context data
    return render(request, 'ana_text.html', {'result': result})
#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#     LocalUploadViewSet
#//////////////////////////////////////////////////////////////   
class LocalUploadViewSet(APIView):
    """
    API endpoint for handling local file uploads and processing.

    This ViewSet provides an endpoint for uploading PDF files, validating them,
    extracting text, performing analysis, and creating Article instances.

    The endpoint is accessible via a POST request to '/upload_files/'.
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ArticlesSerializer

    def post(self, request, *args, **kwargs):
        """
        Endpoint for uploading PDF files, validating them, extracting text,
        performing analysis, and creating Article instances.

        :param HttpRequest request: The request object.

        :return: Response with information about uploaded files and processing result.
        """
        # Create a serializer instance with the request data
        serializer = self.serializer_class(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Get the file from the serializer
            uploaded_file = serializer.validated_data["pdf_File"]
            meta_data = extract_pdf_metadata(uploaded_file)
            titre_meta_data = meta_data["Title"]
            # URL for the file
            file_url = f'http://127.0.0.1:8000/uploaded_media/article_pdfs/{uploaded_file.name}'

            # Ensure the file cursor is at the beginning
            uploaded_file.seek(0)

            # Check if the uploaded PDF is a valid scientific article
            is_valid = is_valid_scientific_pdf(uploaded_file)

            # Handle the case where the PDF is not valid
            if not is_valid:
                return Response({'error': 'Invalid scientific PDF.The provided URL does not lead to a valid scientific article.'}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the file cursor is at the beginning
            uploaded_file.seek(0)

            # Extract text from the uploaded PDF
            pdf_text, f_txt, l_txt = extract_text_from_pdf(uploaded_file)

            # Perform analysis on pdf_text
            analysis_result = extract_article_info(pdf_text, f_txt, l_txt)
 
            #date_str = analysis_result.get('date', '')
            #date_obj = parse_and_validate_date(date_str)
            titre = analysis_result.get('title', '')
            if titre != titre_meta_data:
               titre = titre_meta_data + ' ' + titre
                
            article_data = [
            { 'Titre': titre,
              'Resume': analysis_result.get('abstract', ''),
              'auteurs': analysis_result.get('authors', ''),
              'Institution': analysis_result.get('institutions', ''),
              'date': analysis_result.get('date', ''),
              'MotsCles': analysis_result.get('keywords', ''),
              'text': pdf_text,
              'URL_Pdf': file_url,
              'RefBib': analysis_result.get('references', ''),
            },  
            ]

            # Elasticsearch Indexing
            # Send article data to Elasticsearch 
            send_to_elasticsearch('articles',article_data)
            return Response({'article_data': article_data, 'message': 'Files uploaded and processed successfully and sent to elastic search'}, status=status.HTTP_200_OK)

        # Return serializer errors if the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#     ExternalUploadViewSet
#//////////////////////////////////////////////////////////////
    
class ExternalUploadViewSet(APIView):
    """
    API endpoint for handling external file uploads via URL and processing.

    This ViewSet provides an endpoint for uploading PDF files from a URL,
    downloading them, validating, extracting text, performing analysis,
    and creating Article instances.

    The endpoint is accessible via a POST request to '/upload_url/'.
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ArticlesSerializer

    def post(self, request, *args, **kwargs):
        """
        Endpoint for uploading PDF files from a URL, downloading them,
        validating, extracting text, performing analysis, and creating Article instances.

        :param HttpRequest request: The request object.

        :return: Response with information about the uploaded file and processing result.
        """
        # Create a serializer instance with the request data
        serializer = self.serializer_class(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Get the file URL from the serializer
            url_file = serializer.validated_data["URL_Pdf"]

            # Check if the URL is provided
            if not url_file:
                return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Download the file from the URL
            article_file = download_pdf_from_url(url_file)

            if not article_file:
               return Response({'error': 'Failed to download PDF from the URL'}, status=status.HTTP_400_BAD_REQUEST)

            
            # Ensure the file cursor is at the beginning
            article_file.seek(0)

            # Check if the uploaded PDF is a valid scientific article
            is_valid = is_valid_scientific_pdf(article_file)

            if not is_valid:
                # Handle the case where the PDF is not valid
                return Response({'error': 'Invalid scientific PDF.The provided URL does not lead to a valid scientific article.'}, status=status.HTTP_400_BAD_REQUEST)

            # Get the URL to the uploaded file in the media root
            file_url = url_file

            # Ensure the file cursor is at the beginning
            article_file.seek(0)

            # Extract text from the downloaded PDF
            pdf_text, f_txt, l_txt = extract_text_from_pdf(article_file)

            # Perform analysis on pdf_text
            analysis_result = extract_article_info(pdf_text, f_txt, l_txt)

            date_str = analysis_result.get('date', '')
            date_obj = parse_and_validate_date(date_str)

            # Create Article instance
            article = Articles.objects.create(
                    Titre=analysis_result.get('title', ''),
                    date=date_obj,
                    auteurs=analysis_result.get('authors', ''),
                    Resume=analysis_result.get('abstract', ''),
                    Institution=analysis_result.get('institutions', ''),
                    RefBib=analysis_result.get('references', ''),
                    URL_Pdf=file_url,
                )

            # Save the uploaded file along with the article
            article.pdf_File.save(article_file.name, article_file)

            article.save()

                # Elasticsearch Indexing (Uncomment if needed)
                # send_to_elasticsearch('articles', '_doc', {
                #     'title': analysis_result.get('title', ''),
                #     'date': analysis_result.get('date', ''),
                #     'abstract': analysis_result.get('abstract', ''),
                #     'institutions': analysis_result.get('institutions', ''),
                #     'references': analysis_result.get('references', ''),
                #     'authors': analysis_result.get('authors', ''),
                #     'pdf_text': pdf_text,
                # })

            return Response({'result': analysis_result, 'message': 'Files uploaded and processed successfully and sent to elastic search .'},
                                status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to download PDF from the URL'}, status=status.HTTP_400_BAD_REQUEST)

#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#  LogoutView   
#//////////////////////////////////////////////////////////////
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
'''class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('NomUtilisateur')
        password = request.data.get('MotDePasse')

        user = authenticate(request, NomUtilisateur=username, MotDePasse=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)'''
            
#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#  LoginView   
#//////////////////////////////////////////////////////////////
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Fetch user by username
        try:
            user = Utilisateurs.objects.get(NomUtilisateur=username)
        except Utilisateurs.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.MotDePasse):
            # If user is authenticated, log them in
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # If authentication fails, return an error response
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#--------------------------------------------------------------------------------