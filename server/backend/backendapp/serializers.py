from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris
from django.core.validators import FileExtensionValidator
from django.db import models


class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articles
        fields = ('URL_Pdf','pdf_File','Titre','Resume','auteurs','Institution','date','text','RefBib')

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'
