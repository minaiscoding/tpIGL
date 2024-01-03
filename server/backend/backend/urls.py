from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
#-----------------------------------------------------------------------------------------------#
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
#-----------------------------------------------------------------------------------------------#

# Create a schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Articlo's backend",
        default_version='v1',
        description="The official API docummentation for articlo",

        contact=openapi.Contact(email="la_khadir@esi.dz"),

    ),
    public=True,
)
#-----------------------------------------------------------------------------------------------#
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backendapp.urls')),
    #-----------------------------------------------------------------------------------------------#
    # Add the Swagger and Redoc URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

