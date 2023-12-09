from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris

class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = [
            'Titre',
            'Resume',
            'auteurs',
            'Institution',
           
        ]

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'
