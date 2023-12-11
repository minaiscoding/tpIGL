from rest_framework import generics
from .models import Utilisateurs, Articles, Favoris
from .serializers import UtilisateursSerializer, ArticlesSerializer, FavorisSerializer
from rest_framework import status
from rest_framework.views import APIView
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from rest_framework.response import Response

class UtilisateursListView(generics.ListAPIView):
    queryset = Utilisateurs.objects.all()
    serializer_class = UtilisateursSerializer

class ArticlesListView(generics.ListAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

class FavorisListView(generics.ListAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer
