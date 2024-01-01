from django.urls import path,include
#-----------------------------------------------------------------------------------------------
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, UtilisateursListView, ArticlesListView, FavorisListView, SearchView,LocalUploadViewSet,ExternalUploadViewSet,ModerateursAdd,Moderateurs,ModerateursUpdate,ModerateurDelete
#-----------------------------------------------------------------------------------------------# Import necessary modules from drf-yasg
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('search/', SearchView.as_view(), name='article_search'),
    
    #--------------------------------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #---------------------------------------------------#
    #--------------------------------------------------------------------------------------------------#
    path('articles_ctrl/local-upload/', LocalUploadViewSet.as_view(), name='local-upload'), 
    path('articles_ctrl/external-upload/', ExternalUploadViewSet.as_view(), name='external-upload'),
    #--------------------------------------------------------------------------------------------------#
    path('login/', LoginView.as_view(), name='login'),

    # Add the Swagger and Redoc URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #--------------------------------------------------------------------------------------------------#
    #----------------------# ModerateursControler  #---------------------------------------------------#
    #--------------------------------------------------------------------------------------------------#
    path('moderateurs/', Moderateurs.as_view(), name='moderateurs-add'),
    path('moderateurs/add', ModerateursAdd.as_view(), name='moderateurs-add'),
    path('moderateurs/update/<int:id>', ModerateursUpdate.as_view(), name='moderateurs-update'),
    path('moderateurs/delete/<int:id>',ModerateurDelete.as_view(), name='moderateurs-delete'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
