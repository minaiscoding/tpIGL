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
                      extract_text_with_ocr,
                      extract_article_info,  
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
#--------------------------------------------------------------------------------------------------------------   
    #------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #-------------------------#
    #------------------------------------------------------------------------#   
#--------------------------------------------------------------------------------------------------------------
#/////////////////////////////////////////////////
#    pdf_text_view : to view the text extracted
#/////////////////////////////////////////////////
def pdf_text_view(request):
    file_path = "C:\\Users\\dell\\Downloads\\105245.pdf"
# way 1
    # extract full text from the pdf
    extracted_text = extract_text_from_pdf(file_path)
# way 2
    # convert pdf pages into images 
    #pdf_images = pdf_to_images(file_path)
    # Extract text using OCR from the pdf's images --> process takes a lot of time it's not recommended
    #extracted_text = extract_text_with_ocr(pdf_images)
    return render(request, 'pdf_text.html', {'text': extracted_text})
#--------------------------------------------------------------------------------------------------------------
#///////////////////////
#     
#///////////////////////
@api_view(['POST'])
def upload_articles(request):
    """
    Endpoint API pour recevoir l’adresse URL des articles PDF ou des fichiers PDF locaux.

    Args:
        request: La requête HTTP entrante.

    Returns:
        Une réponse HTTP avec le statut 200 OK si l’opération d’Upload a réussi, ou le statut 400 Bad Request si l’opération a échoué.
    """

    # Récupération de la liste des fichiers PDF.
    files = request.FILES.getlist("files")

    # Vérification de la validité de la liste des fichiers PDF.
    if not files:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Récupération des fichiers PDF à partir de la liste des fichiers PDF.
    articles = []
    for file in files:
        with open(file, "rb") as f:
            articles.append(PyPDF2.PdfFileReader(f).getPage(0).extractText())

    # Analyser les textes des articles pour extraire les informations caractérisant l’article scientifique.
    information_articles = []
    for article in articles:
        # Extraction du titre de l’article.
        title = nltk.sent_tokenize(article)[0]

        # Extraction des auteurs de l’article.
        authors = nltk.word_tokenize(article)[1:]

        # Extraction du journal dans lequel l’article a été publié.
        journal = nltk.sent_tokenize(article)[2]

        # Extraction de la date de publication de l’article.
        date = nltk.sent_tokenize(article)[3]

        # Extraction du résumé de l’article.
        abstract = article[len(title) + len(authors) + len(journal) + len(date) :]

        information_articles.append({
            "title": title,
            "authors": authors,
            "journal": journal,
            "date": date,
            "abstract": abstract,
        })

    # Envoyer les informations extraites dans un index de recherche dans ElasticSearch.
    #es = Elasticsearch()
    #for information_article in information_articles:
        #es.index(index="articles", doc_type="article", body=information_article)

    return Response(status=status.HTTP_200_OK)
#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#   analize_text_view to view the extracted info of the article  
#//////////////////////////////////////////////////////////////
def analize_text_view(request):
    
    file_path = "C:\\Users\\dell\\Downloads\\105245.pdf"
# way 1
    # Extract text from the PDF file
    pdf_text = extract_text_from_pdf(file_path)

    # Analyze the extracted text
    result = extract_article_info(pdf_text)
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

class LocalUploadViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    @action(detail=False, methods=['POST'])
    def upload_files(self, request):
        uploaded_files = request.FILES.getlist('file')

        results = []
        if not uploaded_files:
            return Response({'error': 'files are required'}, status=status.HTTP_400_BAD_REQUEST)

        for uploaded_file in uploaded_files:
            if not uploaded_file.path.endswith('.pdf'):
                return Response({'error': 'Only PDF files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract text from the uploaded PDF
            pdf_text = extract_text_from_pdf(uploaded_file)
            print(pdf_text)

            # Perform analysis on pdf_text
            analysis_result = extract_article_info(pdf_text)
            print(analysis_result)

            # Generate a tuple for each article (title, date, analysis result)
            article_data = {
                'title': request.data.get('title', ''),
                'date': request.data.get('date', ''),
                'analysis_result': analysis_result,
            }

            print(article_data)

            results.append(article_data)

            print(results)

        # Create Article instances for local files
        for result in results:
            article = Articles.objects.create(
                title=result['title'],
                date=result['date'],
            )

            # Convert local file into an external URL (placeholder for now)
            article.URL_Pdf = f'/media/{uploaded_file.name}'
            print(article.URL_Pdf)
            article.save()

        # Elasticsearch Indexing (placeholder for now)
        # (Send article data to Elasticsearch for indexing)
        # Envoyer les informations extraites dans un index de recherche dans ElasticSearch.
        #es = Elasticsearch()
        #for information_article in information_articles:
        #es.index(index="articles", doc_type="article", body=information_article)

        return Response(results, status=status.HTTP_201_CREATED)
    
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
        articles_data = download_pdf_from_url(url)

        if articles_data:
            results = []

            for article_data in articles_data:
                # Extract text from the downloaded PDF
                pdf_text = extract_text_from_pdf(article_data['pdf_File'])

                # Perform analysis on pdf_text
                analysis_result = extract_article_info(pdf_text)

                # Create an instance of Article (without saving it)
                article_instance = Articles(
                    title=article_data['title'],
                    date=article_data['date'],
                    external_url=url,
                )

                results.append({
                    'title': article_data['title'],
                    'date': article_data['date'],
                    'analysis_result': analysis_result,
                })

            # Elasticsearch Indexing (placeholder for now)
            # (Send article data to Elasticsearch for indexing)
            # Envoyer les informations extraites dans un index de recherche dans ElasticSearch.
            #es = Elasticsearch()
            #for information_article in information_articles:
            #es.index(index="articles", doc_type="article", body=information_article)

            return Response(results, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to download PDF from the URL'}, status=status.HTTP_400_BAD_REQUEST)