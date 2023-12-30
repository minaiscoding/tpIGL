from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UtilisateursListView, ArticlesListView, FavorisListView, SearchView, ArticleDetailView,LoginView



urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('articles/<str:article_id>/', ArticleDetailView.as_view(), name='article-detail'),  # Add this line
    path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('search/', SearchView.as_view(), name='article_search'),
    path('login/', LoginView.as_view(), name='login'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
