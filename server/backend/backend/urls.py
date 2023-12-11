from django.contrib import admin
from django.urls import path, include
#from ArticlesControl.views import pdf_text_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backendapp.urls')),
    # path('pdf-text/', pdf_text_view, name='pdf_text'), for testing 
]