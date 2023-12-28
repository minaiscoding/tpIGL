from rest_framework import serializers
from .models import Utilisateurs, Articles, Favoris




class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateurs
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articles
<<<<<<< HEAD
        fields = ('pdf_File','URL_Pdf','Titre','auteurs','Resume','date','Institution','RefBib')
=======
        fields = '__all__'
>>>>>>> 586a27361392aa78c31e9ca12016ed8150528803

class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'
