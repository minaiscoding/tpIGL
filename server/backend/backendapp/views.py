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


class SearchView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Get the search query from the request parameters
        query = request.GET.get('q', '')

        # Perform the Elasticsearch search
        search = Search(index='articles').query('match', Titre=query)
        response = search.execute()

        # Extract relevant information from search hits
        hits = [{"id": "tested", **hit.to_dict()} for hit in response.hits]

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
                request.user = utilisateur
                print(utilisateur.Role)
                # Check user role and respond accordingly
                if utilisateur.Role == 'admin':
                    return Response({'role': 'admin', 'message': 'Login successful'}, status=status.HTTP_200_OK)
                elif utilisateur.Role == 'moderator':
                    return Response({'role': 'moderator', 'message': 'Login successful'}, status=status.HTTP_200_OK)
                elif utilisateur.Role == 'user':
                    return Response({'role': 'user', 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Utilisateurs.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)          

'''class LoginView(APIView):
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
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)'''
            
            
'''class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        utilisateurs_serializer_data = UtilisateursSerializer(user.user).data if hasattr(user, 'user') else None

        return Response({
            'token': token.key,
            'utilisateurs': utilisateurs_serializer_data
        })'''
'''@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        serializer = CustomUserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)'''
