from django.contrib.auth.hashers import check_password
from rest_framework import generics
from .models import  Articles, Favoris, Utilisateurs
from .serializers import  ArticlesSerializer, FavorisSerializer, AuthTokenSerializer,UtilisateursSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Search
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from elasticsearch import Elasticsearch


@api_view(['DELETE'])
def delete_article(request, pk):
    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        index_name = 'articles'

        es.delete(index=index_name, doc_type='_doc', id=pk)

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class ArticleDetailView(APIView):
    def get(self, request, article_id):
        # Perform the Elasticsearch search to get the article by ID
        search = Search(index='articles').query('term', id=article_id)  # Assuming 'id' is the name of the field in your model
        response = search.execute()

        # Extract relevant information from the search hit
        hit = response.hits[0].to_dict() if response.hits else {}

        return Response(hit)
    
    
    
class FavorisListView(generics.ListAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer


from django.http import JsonResponse

class SearchView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Get the search query from the request parameters
        query = request.GET.get('q', '')

        # Get start and end dates from the request parameters
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        # Get the selected filter type from the request parameters
        filter_type = request.GET.get('filter_type', 'Titre')

        # Initialize the date range filter as an empty list
        date_range_filter = []

        # Check if start_date and end_date are not empty before including them in the filter
        if start_date and end_date:
            date_range_filter = [{'range': {'date': {'gte': start_date, 'lte': end_date}}}]

        # Perform the Elasticsearch search with dynamic query and date range filter
        search = Search(index='articles').query('bool', filter=date_range_filter).query('match', **{filter_type: query})

        try:
            response = search.execute()

            # Extract relevant information from search hits
            hits = [{'id': hit.meta.id, **hit.to_dict()} for hit in response.hits]

            # Serialize the search results using your existing serializer
            serializer = ArticlesSerializer(data=hits, many=True)
            serializer.is_valid()

            # Return the serialized results as JSON
            return Response(serializer.data)

        except Exception as e:
            # Handle exceptions, log them, or return an appropriate error response
            return JsonResponse({'error': str(e)}, status=500)

    


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
    @csrf_exempt  # Use this decorator if you disable CSRF in your settings or for testing purposes
    def post(self, request, *args, **kwargs):
        nom_utilisateur = request.data.get('NomUtilisateur')
        password = request.data.get('MotDePasse')

        # Debug: Print request data
        print('Request data:', request.data)

        # Debug: Print user model fields
        print('User model fields:', Utilisateurs._meta.get_fields())

        try:
            # Retrieve user based on the provided username
            utilisateur = Utilisateurs.objects.get(NomUtilisateur=nom_utilisateur)
            
            # Check if the provided password matches the stored password
            if check_password(password, utilisateur.MotDePasse):
                # Login the user
                #request.user = utilisateur
               # Serialize the user instance
                serializer = UtilisateursSerializer(utilisateur)

                # Add the role information to the response
                response_data = {
                    'role': utilisateur.Role,
                    'message': 'Login successful',
                    'utilisateur': serializer.data,  # Include the serialized user data
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Utilisateurs.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)  