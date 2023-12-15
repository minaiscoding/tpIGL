from rest_framework import generics
from .models import Utilisateurs, Articles, Favoris
from .serializers import UtilisateursSerializer, ArticlesSerializer, FavorisSerializer
<<<<<<< HEAD
from rest_framework import status
from rest_framework.views import APIView
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from rest_framework.response import Response
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Search
from rest_framework.renderers import JSONRenderer

>>>>>>> origin/main

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