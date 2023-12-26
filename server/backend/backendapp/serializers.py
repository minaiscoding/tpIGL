from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris

class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articles
        fields = ('pdf_File','URL_Pdf','Titre','Resume','date','Institution','RefBib')

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'
