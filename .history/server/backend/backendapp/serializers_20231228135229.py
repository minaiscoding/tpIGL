from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris

class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'

class FavorisSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField()