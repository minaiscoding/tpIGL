from rest_framework import generics
from .models import Utilisateurs, Articles, Favoris
from .serializers import UtilisateursSerializer, ArticlesSerializer, FavorisSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Search

class UtilisateursListView(generics.ListAPIView):
    queryset = Utilisateurs.objects.all()
    serializer_class = UtilisateursSerializer

class ArticlesListView(generics.ListAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

class FavorisListView(generics.ListAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer
class SearchView(APIView):
    def get(self, request):
        # Get the search query from the request parameters
        query = request.GET.get('q', '')

        # Perform the Elasticsearch search
        search = Search(index='articles_index').query('match', Titre=query)
        response = search.execute()

        # Serialize the search results using your existing serializer
        serializer = ArticlesSerializer(response.hits, many=True)

        # Return the serialized results as JSON
        return Response(serializer.data)