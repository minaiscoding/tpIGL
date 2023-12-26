import json
from rest_framework import generics
from .models import Utilisateurs, Articles, Favoris
from .serializers import UtilisateursSerializer, ArticlesSerializer, FavorisSerializer
from rest_framework import status
from rest_framework.views import APIView
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Search
from rest_framework.renderers import JSONRenderer

#------------------------------------------------------------
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import requests
import PyPDF2
import nltk

from elasticsearch import Elasticsearch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


import os
import requests

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
from .models import Articles
from .serializers import  ArticlesSerializer
#--------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
#---------------------------------------------------------------------------------
import os
from rest_framework import viewsets, status
from rest_framework.decorators import action
#------------------------------------------------------------------

from .utils import (  extract_text_from_pdf,
                      download_pdf_from_url,
                      pdf_to_images,
                      extract_pdf_metadata,
                      extract_text_with_ocr,
                      is_valid_scientific_pdf,
                      extract_article_info, 
                      extract_text_from_pdf_url, 
                   )
#--------------------------------------------------------------------------------------------------------------

class UtilisateursListView(generics.ListAPIView):
    queryset = Utilisateurs.objects.all()
    serializer_class = UtilisateursSerializer

class ArticlesListView(generics.ListAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

class FavorisListView(generics.ListAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer


class SearchView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Get the search query from the request parameters
        query = request.GET.get('q', '')

        # Perform the Elasticsearch search
        search = Search(index='articles').query('match', Titre=query)
        response = search.execute()

        # Extract relevant information from search hits
        hits = [{'id': hit.meta.id, **hit.to_dict()} for hit in response.hits]

        # Serialize the search results using your existing serializer
        serializer = ArticlesSerializer(data=hits, many=True)
        serializer.is_valid()

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

#--------------------------------------------------------------------------------------------------------------   
    #------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #-------------------------#
    #------------------------------------------------------------------------#   
#--------------------------------------------------------------------------------------------------------------
#///////////////////////
# scientific_pdf_view
#///////////////////////

def scientific_pdf_view(request):
    # Call the test_scientific_pdf function to get the validation result
    #url='C:\\Users\\dell\\Downloads\\articles_sci\\ARTICLE7.pdf'
    url='C:\\Users\\dell\\Downloads\\Articles\\EchantillonsArticles\\Article_05.pdf'
    is_valid = is_valid_scientific_pdf(url)

    # Render the template with the context data
    return render(request, 'test_scientific_pdf.html', {'is_valid': is_valid})
#/////////////////////////////////////////////////
#    pdf_text_view : to view the text extracted
#/////////////////////////////////////////////////
def pdf_text_view(request):
    file_path = "C:\\Users\\dell\\Downloads\\Articles\\EchantillonsArticles\\Article_05.pdf"

    #url ="https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9721302"
    
    #if url:

# way 1
    # extract full text from the pdf
    #extracted_text,f_txt,l_txt = extract_text_from_pdf_url(url)
    extracted_text,f_txt,l_txt = extract_text_from_pdf(file_path)
    #else:
    #print("Failed to download PDF from the provided URL.")
    #   extracted_text="null"
    #   f_txt="null"
    #   l_txt ="null"

# way 2
    # convert pdf pages into images 
    #pdf_images = pdf_to_images(file_path)
    # Extract text using OCR from the pdf's images --> process takes a lot of time it's not recommended
    #extracted_text = extract_text_with_ocr(pdf_images)
    return render(request, 'pdf_text.html', {'full_text': extracted_text,'first_pages':f_txt,'last_pages':l_txt})
#-------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#   analize_text_view to view the extracted info of the article  
#//////////////////////////////////////////////////////////////

def analize_text_view(request):

    file_path = "C:\\Users\\dell\\Downloads\\Articles\\EchantillonsArticles\\Article_05.pdf"
    #url ="https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9721302"

# way 1
    #if url:

    #meta = extract_pdf_metadata(url)
    # Extract text from the PDF file
    #pdf_text,f_txt,l_txt = extract_text_from_pdf_url(url)
    pdf_text,f_txt,l_txt = extract_text_from_pdf(file_path)

    # Analyze the extracted text
    result = extract_article_info(pdf_text,f_txt,l_txt)
    #else:
    #print("Failed to download PDF from the provided URL.")
# way 2
    # convert pdf pages into images 
    #pdf_images = pdf_to_images(file_path)
    # Extract text using OCR from the pdf's images --> process takes a lot of time it's not recommended
    #pdf_text = extract_text_with_ocr(pdf_images)
    # Analyze the extracted text
    #result = extract_article_info(pdf_text)
    # Render the template with the extracted information
    return render(request, 'ana_text.html', {'result': result,})


#--------------------------------------------------------
from django.core.files.storage import default_storage
class LocalUploadViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    @action(detail=False, methods=['POST'])
    def upload_files(self, request):
        uploaded_files = request.FILES.getlist('pdf_file')

        if not uploaded_files:
            return Response({'error': 'Files are required.'}, status=status.HTTP_400_BAD_REQUEST)
        response_data = []
        for uploaded_file in uploaded_files:
            if not uploaded_file.name.lower().endswith('.pdf'):
                return Response({'error': 'Only PDF files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

            # Construct the file path using the uploaded file name
            path = default_storage.save(f'/article_pdfs/{uploaded_file.name}', uploaded_file)
            
            # Check if the uploaded PDF is a valid scientific article
            is_valid = is_valid_scientific_pdf(path)
            
            if not is_valid:
                # Handle the case where the PDF is not valid
                return Response({'error': 'Invalid scientific PDF.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract text from the uploaded PDF
            pdf_text,f_txt,l_txt = extract_text_from_pdf(path)
            

            # Perform analysis on pdf_text
            analysis_result = extract_article_info(pdf_text,f_txt,l_txt)
            
 
            article_data = {
                'Titre': analysis_result.get('title', ''),
                'date': analysis_result.get('date', ''),
                'auteurs':analysis_result.get('authors', ''),
                'resume':analysis_result.get('abstract', ''),
                'Institution':analysis_result.get('institutions', ''),
                'MotsCles':analysis_result.get('keywords', ''),
                'RefBib':analysis_result.get('references', ''),
                'Text_integral': pdf_text,
                #'analyse': json.dumps(analysis_result),            
            }
            print(article_data) 
            # Create Article instances 
            article = Articles.objects.create(
                Titre=article_data['Titre'],
                date=article_data['date'],
                #auteurs=article_data['auteurs'],
                Resume=article_data['resume'],
                Institution=article_data['Institution'],
                #MotsCles=article_data['MotsCles'],
                RefBib=article_data['RefBib'],      
            )
            article.save()

        # Get the actual filesystem path where the file is stored
        actual_path = default_storage.path(path)

        # Add file information to the response data
        response_data.append({
                'file_name': uploaded_file.name,
                'file_path': actual_path,
                'pdf_text': pdf_text,
                # Add other information you want to include
            })

        # Elasticsearch Indexing (placeholder for now)
        # (Send article data to Elasticsearch for indexing)
        # es = Elasticsearch()
        # for information_article in information_articles:
        #     es.index(index="articles", doc_type="article", body=information_article)

        return Response({'files': response_data, 'message': 'Files uploaded and processed successfully.'}, status=status.HTTP_200_OK)
    

    
#-----------------------------------------------------------------------------------
    
class ExternalUploadViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    @action(detail=False, methods=['POST'])
    def upload_url(self, request):
        url = request.data.get('URL Pdf')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Download the file from the URL
        article = download_pdf_from_url(url)


        if article:  
                # Extract text from the downloaded PDF
                pdf_text,f_txt,l_txt = extract_text_from_pdf(article)

                # Perform analysis on pdf_text
                analysis_result = extract_article_info(pdf_text,f_txt,l_txt)

                # Generate a tuple for each article
                article_data = {
                'Titre': analysis_result.get('title', ''),
                'date': analysis_result.get('date', ''),
                'auteurs':analysis_result.get('authors', ''),
                'resume':analysis_result.get('abstract', ''),
                'Institution':analysis_result.get('institutions', ''),
                'MotsCles':analysis_result.get('keywords', ''),
                'RefBib':analysis_result.get('references', ''),
                'Text_integral': pdf_text,
                #'analyse': json.dumps(analysis_result),            
            }
                print(article_data)

                # Create Article instances
                article = Articles.objects.create(
                       Titre=article_data['Titre'],
                       date=article_data['date'],
                       #auteurs=article_data['auteurs'],
                       Resume=article_data['resume'],
                       Institution=article_data['Institution'],
                       #MotsCles=article_data['MotsCles'],
                       RefBib=article_data['RefBib'],           
            )

            # Elasticsearch Indexing (placeholder for now)
            # (Send article data to Elasticsearch for indexing)
            # Envoyer les informations extraites dans un index de recherche dans ElasticSearch.
            #es = Elasticsearch()
            #for information_article in information_articles:
            #es.index(index="articles", doc_type="article", body=information_article)
                print(analysis_result)
                return Response(analysis_result,status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to download PDF from the URL'}, status=status.HTTP_400_BAD_REQUEST)