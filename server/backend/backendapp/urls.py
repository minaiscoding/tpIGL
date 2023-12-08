from django.urls import path
from .views import UtilisateursListView, ArticlesListView, FavorisListView, SearchView

urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('search/', SearchView.as_view(), name='article_search'),
]
