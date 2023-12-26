from django.contrib.auth.hashers import check_password
from rest_framework import generics
from .models import Utilisateurs, Articles, Favoris
from .serializers import UtilisateursSerializer, ArticlesSerializer, FavorisSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Search
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.contrib.auth import authenticate, login, logout



class UtilisateursListView(generics.ListAPIView):
    queryset = Utilisateurs.objects.all()
    serializer_class = UtilisateursSerializer

class ArticlesListView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Perform the Elasticsearch search to get all articles
        search = Search(index='articles').query('match_all')
        response = search.execute()

        # Extract relevant information from search hits
        hits = [{'id': hit.meta.id, **hit.to_dict()} for hit in response.hits]
        

        # Serialize the search results using your existing serializer
        serializer = ArticlesSerializer(data=hits, many=True)
        serializer.is_valid()

        # Return the serialized results as JSON
        return Response(serializer.data)


class FavorisListView(generics.ListAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer


class SearchView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Get the search query from the request parameters
        query = request.GET.get('q', '')

        # Perform the Elasticsearch search
        search = Search(index='articles').query('match', Titre=query)
        response = search.execute()

        # Extract relevant information from search hits
        hits = [{'id': hit.meta.id, **hit.to_dict()} for hit in response.hits]

        # Serialize the search results using your existing serializer
        serializer = ArticlesSerializer(data=hits, many=True)
        serializer.is_valid()

        # Return the serialized results as JSON
        return Response(serializer.data)


    
    


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
'''class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('NomUtilisateur')
        password = request.data.get('MotDePasse')

        user = authenticate(request, NomUtilisateur=username, MotDePasse=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)'''
            

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Fetch user by username
        try:
            user = Utilisateurs.objects.get(NomUtilisateur=username)
        except Utilisateurs.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.MotDePasse):
            # If user is authenticated, log them in
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # If authentication fails, return an error response
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)