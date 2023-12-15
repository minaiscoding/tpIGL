from django.urls import path, include
from .views import UploadArticleView,analize_text_view,pdf_text_view,pdf_metadata_view,scientific_pdf_view

urlpatterns = [

    path('upload/', UploadArticleView.as_view(), name='upload_article'),# to be tested later
    path('ana-text/', analize_text_view, name='ana_text'), #for testing 
    path('pdf-text/', pdf_text_view, name='pdf_text'), #for testing 
    path('pdf-mata/', pdf_metadata_view, name='pdf_meta'), #for testing 
    path('scientific-pdf/', scientific_pdf_view, name='scientific_pdf'),#for testing


]