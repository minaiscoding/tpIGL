from rest_framework import serializers
from .models import Articles, Favoris, Utilisateurs

class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'
        
class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'
        

class AuthTokenSerializer(serializers.Serializer):
    NomUtilisateur = serializers.CharField()
    MotDePasse = serializers.CharField()
