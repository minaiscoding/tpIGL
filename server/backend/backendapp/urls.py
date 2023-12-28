from django.urls import path,include
from .views import UtilisateursListView, ArticlesListView, FavorisListView,SearchView,LocalUploadViewSet,ExternalUploadViewSet
#-----------------------------------------------------------------------------------------------
from .views import pdf_text_view,analize_text_view,scientific_pdf_view,pdf_metadata_view
#-----------------------------------------------------------------------------------------------
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, UtilisateursListView, ArticlesListView, FavorisListView, SearchView

urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('search/', SearchView.as_view(), name='article_search'),
    
    #------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #-------------------------#
    #------------------------------------------------------------------------#
    path('articles_ctrl/pdf-text/', pdf_text_view, name='pdf_text'), #tested with ocr and with fitz
    path('articles_ctrl/ana-text/', analize_text_view, name='ana_text'), #for testing
    path('articles_ctrl/sci_art/', scientific_pdf_view, name='sci_art'), #for testing
    path('articles_ctrl/meta_data/', pdf_metadata_view, name='meta_data'), #for testing

    path('articles_ctrl/local-upload/', LocalUploadViewSet.as_view(), name='local-upload'), 
    path('articles_ctrl/external-upload/', ExternalUploadViewSet.as_view(), name='external-upload'),
    
    

    path('login/', LoginView.as_view(), name='login'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
