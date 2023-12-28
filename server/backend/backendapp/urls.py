from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UtilisateursListView, ArticlesListView, FavorisListView, SearchView, ArticleDetailView,LoginView,delete_article

urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('articles/<str:article_id>/', ArticleDetailView.as_view(), name='article-detail'),  # Add this line
    path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('search/', SearchView.as_view(), name='article_search'),
    path('login/', LoginView.as_view(), name='login'),
    #path('token/', LoginAPI.as_view(), name='token-view'),
    #path('api/login/', custom_login, name='custom_login'),
    #path('api/register/', register_user, name='register_user'),
     path('api/articles/<str:pk>/', delete_article, name='delete-article'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
