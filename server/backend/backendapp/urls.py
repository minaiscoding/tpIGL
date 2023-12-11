from django.urls import path
from .views import UtilisateursListView, ArticlesListView, FavorisListView
from ArticlesControl.views import UploadArticleView


urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('upload/', UploadArticleView.as_view(), name='upload_article'),# to be tested later
    
    
    
]
