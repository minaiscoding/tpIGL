from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleUploadViewSet,UploadArticleView,analize_text_view,pdf_text_view,pdf_metadata_view,scientific_pdf_view
from .views import LocalFileUploadView, ExternalURLUploadView

router = DefaultRouter()
router.register(r'article-upload', ArticleUploadViewSet, basename='article-upload')

urlpatterns = [

    path('', include(router.urls)),# to be tested later
    path('ana-text/', analize_text_view, name='ana_text'), #for testing 
    path('pdf-text/', pdf_text_view, name='pdf_text'), #for testing 
    path('pdf-mata/', pdf_metadata_view, name='pdf_meta'), #for testing 
    path('scientific-pdf/', scientific_pdf_view, name='scientific_pdf'),#for testing
    
    path('upload/local/', LocalFileUploadView.as_view(), name='local-file-upload'),
    path('upload/external/', ExternalURLUploadView.as_view(), name='external-url-upload'),

]