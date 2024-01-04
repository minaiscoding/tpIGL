from django.urls import path,include
#-----------------------------------------------------------------------------------------------
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, UtilisateursListView, ArticlesListView, SaveFavoriteView, FavoriteArticleListView , SearchView,LocalUploadViewSet,ExternalUploadViewSet
#-----------------------------------------------------------------------------------------------

urlpatterns = [
    path('saveFavorite/', SaveFavoriteView.as_view(), name='save_favorite'),
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
 #path('articles/', ArticlesListView.as_view(), name='articles-list'),
   # path('articles/<str:article_id>/', ArticleDetailView.as_view(), name='article-detail'),  # Add this line
    
    path('favoris/<int:user_id>/', FavoriteArticleListView.as_view(), name='user-favorite-articles'),
    path('search/', SearchView.as_view(), name='article_search'), 
    #--------------------------------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #---------------------------------------------------#
    #--------------------------------------------------------------------------------------------------#
    path('articles_ctrl/local-upload/', LocalUploadViewSet.as_view(), name='local-upload'), 
    path('articles_ctrl/external-upload/', ExternalUploadViewSet.as_view(), name='external-upload'),
    #--------------------------------------------------------------------------------------------------#
    path('login/', LoginView.as_view(), name='login'),

]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
