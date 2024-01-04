from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris ,ArticleFile
from django.db import models


class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'
        
class ArticlesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articles
        fields = '__all__'

class UploadArticlesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ArticleFile
        fields = ('URL_Pdf','pdf_File')

class FavoriteArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = ['UtilisateurID', 'ArticleID']
        

class AuthTokenSerializer(serializers.Serializer):
    NomUtilisateur = serializers.CharField()
    MotDePasse = serializers.CharField()
