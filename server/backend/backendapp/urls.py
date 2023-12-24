from django.urls import path, include
from .views import UtilisateursListView, ArticlesListView, FavorisListView, SearchView,LocalUploadViewSet,ExternalUploadViewSet
from .views import upload_articles,pdf_text_view,analize_text_view

#-----------------------------------------------------------------------------------------------
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'local-upload', LocalUploadViewSet, basename='local-upload')
router.register(r'external-upload', ExternalUploadViewSet, basename='external-upload')

urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('search/', SearchView.as_view(), name='article_search'),

    #------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #-------------------------#
    #------------------------------------------------------------------------#
    path('upload_articles/', upload_articles, name='upload_articles'),
    path('articles_ctrl/pdf-text/', pdf_text_view, name='pdf_text'), #tested with ocr and with fitz
    path('articles_ctrl/ana-text/', analize_text_view, name='ana_text'), #for testing
    path('upload_files/',include(router.urls)),
    




    
    

]









