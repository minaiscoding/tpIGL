from django.contrib import admin
from django.urls import path, include
from ArticlesControl.views import analize_text_view,pdf_text_view,pdf_metadata_view,scientific_pdf_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backendapp.urls')),
    path('api/articles_control', include('ArticlesControl.urls')),

]