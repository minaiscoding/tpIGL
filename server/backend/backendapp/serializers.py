from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris

class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('URL_Pdf', 'pdf_File')
        

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'
