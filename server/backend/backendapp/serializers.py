from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris

class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    PDF_File = serializers.FileField()
    class Meta:
        model = Articles
<<<<<<< HEAD
        fields = '__all___'
=======
        fields = [
            'Titre',
            'Resume',
            'auteurs',
            'Institution',
           
        ]
>>>>>>> origin/main

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'
