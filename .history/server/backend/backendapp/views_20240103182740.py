import os
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework.generics import ListAPIView
#--------------------------------------------------------------------------------
from .models import Utilisateurs, Articles, Favoris
from .serializers import UtilisateursSerializer, ArticlesSerializer,UploadArticlesSerializer, FavoriteArticleSerializer
#--------------------------------------------------------------------------------
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import action,api_view, permission_classes
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
#--------------------------------------------------------------------------------
from elasticsearch_dsl import Search
#------------------------------------------------------------------
from .utils import (  extract_text_from_pdf,
                      extract_pdf_metadata,
                      is_valid_scientific_pdf,
                      extract_article_info,
                      download_pdf_from_url,
                      send_to_elasticsearch, 
                       parse_metadata_date, 
                      upload_article_process,          
                   )
import string
#--------------------------------------------------------------------------------
from rest_framework.decorators import schema, parser_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#--------------------------------------------------------------------------------------------------------------

#                               views.py --> api endpoints

#--------------------------------------------------------------------------------------------------------------

class UtilisateursListView(generics.ListAPIView):
    queryset = Utilisateurs.objects.all()
    serializer_class = UtilisateursSerializer
#--------------------------------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------

class SearchView(APIView):
    renderer_classes = [JSONRenderer]
    @swagger_auto_schema(
        operation_summary="Perform a search",
        operation_description="Perform a search based on the provided query parameters.",
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date for date range filter", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date for date range filter", type=openapi.TYPE_STRING),
            openapi.Parameter('filter_type', openapi.IN_QUERY, description="Filter type", type=openapi.TYPE_STRING),
        ],
    )

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

#--------------------------------------------------------------------------------------------------------------#  
 
    #------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #-------------------------#
    #------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------#

#//////////////////////////////////////////////////////////////
#     LocalUploadViewSet
#//////////////////////////////////////////////////////////////   
class LocalUploadViewSet(APIView):
    """
    API endpoint for handling local file uploads and processing.

    This ViewSet provides an endpoint for uploading PDF files of research scientific papers, validating them,
    extracting text, performing analysis, and sending the information of the analysis to a search index of Elasticsearch.

    The endpoint is accessible via a POST request to 'api/articles_ctrl/local-upload/'.
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadArticlesSerializer

    @swagger_auto_schema(
        request_body=UploadArticlesSerializer,
        operation_summary="Upload and process a PDF file of research scientific papers.",
        operation_description="This endpoint handles the upload, validation, text extraction, analysis, and indexing of scientific articles.",
        responses={200: "OK", 400: "Bad Request"},
    )
    def post(self, request, *args, **kwargs):
        """
        Endpoint for uploading one PDF file of research scientific papers, validating them, extracting text,
        performing analysis, and sending the information of the analysis to a search index of Elasticsearch.

        :param HttpRequest request: The request object -->  file object.

        :return: Response with information about uploaded file and processing result.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['pdf_File']
            uploaded_file.seek(0)
            is_valid = is_valid_scientific_pdf(uploaded_file)

            if not is_valid:
                return Response({'error': 'Invalid scientific PDF. The provided file does not lead to a valid scientific article.'}, status=status.HTTP_400_BAD_REQUEST)

            article_data = upload_article_process(uploaded_file)
            send_to_elasticsearch('articles', article_data)

            
            # Save the PDF file to the media root   
            article = serializer.save()
            article.delete()

            file_url = article_data[0]['URL_Pdf']

            return Response({
                'article_data': article_data,
                'url_pdf': file_url,
                'message': 'Files uploaded and processed successfully and sent to Elasticsearch'
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
#--------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////
#     ExternalUploadViewSet
#//////////////////////////////////////////////////////////////
    
class ExternalUploadViewSet(APIView):
    """
    API endpoint for handling external PDF file of research scientific papers uploads via URL and processing.

    This ViewSet provides an endpoint for uploading PDF files from a URL,
    downloading them, validating, extracting text, performing analysis,
    and sending the information of the analysis to a search index of Elasticsearch.

    The endpoint is accessible via a POST request to 'articles_ctrl/external-upload/'.
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadArticlesSerializer

    @swagger_auto_schema(
        request_body= UploadArticlesSerializer,
        operation_summary="Upload and process a PDF file of research scientific papers from a URL.",
        operation_description="This endpoint handles the download, validation, text extraction, analysis, and indexing of scientific articles from an external URL.",
        responses={200: "OK", 400: "Bad Request"},
    )
    def post(self, request, *args, **kwargs):
        """
        Endpoint for uploading one PDF file of research scientific papers from a URL, downloading them,
        validating, extracting text, performing analysis, and sending the information of the analysis to a search index of Elasticsearch.

        :param HttpRequest request: The request object --> file object.

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
                return Response({'error': 'Échec du téléchargement du PDF depuis l\'URL.'}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the file cursor is at the beginning
            article_data = []

            # Check if the uploaded PDF is a valid scientific article
            is_valid = is_valid_scientific_pdf(article_file)

            if not is_valid:
                # Handle the case where the PDF is not valid
                return Response(
                    {'error': 'PDF scientifique invalide. L\'URL fournie ne mène pas à un article scientifique valide.'},
                    status=status.HTTP_400_BAD_REQUEST)

            # Get the URL to the uploaded file in the media root
            file_url = url_file

            # Extract metadata from the downloaded PDF
            meta_data = extract_pdf_metadata(article_file)
            titre_meta_data = meta_data.get("Title","")
            date_meta_data = meta_data.get("CreationDate","")

            # Extract text from the downloaded PDF
            pdf_text, f_txt, l_txt = extract_text_from_pdf(article_file)

            # Perform analysis on pdf_text
            analysis_result = extract_article_info(pdf_text, f_txt, l_txt)

            # Combine title/date from metadata and analysis result

            titre = analysis_result.get('title', '')
            date = analysis_result.get('date', '')

            # Define a translation table to remove specific characters
            translator = str.maketrans('', '', string.whitespace + "''’")

            # Remove spaces and specified characters from titre and titre_meta_data
            titre_without_spaces = titre.translate(translator)
            titre_meta_data_without_spaces = titre_meta_data.translate(translator)

            # Compare the modified strings
            if titre_without_spaces != titre_meta_data_without_spaces:
               titre = titre_meta_data + ' ' + titre


            if date_meta_data and not date :
               date = parse_metadata_date(date_meta_data)

            # Prepare data for Article creation
            article_data = [{
                'Titre': titre,
                'Resume': analysis_result.get('abstract', ''),
                'auteurs': analysis_result.get('authors', ''),
                'Institution': analysis_result.get('institutions', ''),
                'date': analysis_result.get('date', ''),
                'MotsCles': analysis_result.get('keywords', ''),
                'text': pdf_text,
                'URL_Pdf': file_url,
                'RefBib': analysis_result.get('references', ''),
            }]


            # Elasticsearch Indexing
            # Send article data to Elasticsearch
            send_to_elasticsearch('articles', article_data)

            return Response( {
                             'article_data': article_data,
                             'message': 'Files uploaded and processed successfully and sent to Elasticsearch'
                             },
                             status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Échec du téléchargement du PDF depuis l\'URL.'},
                            status=status.HTTP_400_BAD_REQUEST)

#--------------------------------------------------------------------------------
#/////////////////////////
#  LogoutView   
#/////////////////////////
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
#/////////////////////////
#  LoginView   
#/////////////////////////
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
from rest_framework.permissions import IsAuthenticated

class SaveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Get the articleId and userId from the request data
            article_id = request.data.get("articleId")
            user_id = request.data.get("userId")

            # Check if the article is already marked as a favorite for this user
            existing_favorite = Favoris.objects.filter(
                ArticleID=article_id, UtilisateursID=user_id
            ).exists()

            if not existing_favorite:
                # If not, create a new favorite entry in the database
                favorite = Favoris.objects.create(
                    ArticleID=article_id, UtilisateursID=user_id
                )
                serializer = FavoriteArticleSerializer(favorite)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # If already favorited, return a 400 Bad Request response
                return Response(
                    {"detail": "Article is already marked as a favorite."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"detail": f"Error saving favorite article: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    
class FavoriteArticleListView(ListAPIView):
    serializer_class = FavoriteArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the favorite articles for the authenticated user
        return Favoris.objects.filter(UtilisateurID=self.request.user)
    
    #-----------------------------function to retrieve all the user's favorite articles IDs-------------------------------
    
    from django.shortcuts import get_object_or_404
    def get_user_favorite_article_ids(user_id):
    
        user = get_object_or_404(Utilisateurs, id=user_id)

        # Retrieve the favorite articles for the user
        favorite_articles = Favoris.objects.filter(user=user)

        # Extract and return the article IDs
        article_ids = [favorite.article.id for favorite in favorite_articles]

        return article_ids


