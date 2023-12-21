from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backendapp.urls')),
    path('api/articles_control/', include('ArticlesControl.urls')),

]