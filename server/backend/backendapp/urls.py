from django.urls import path,include
#-----------------------------------------------------------------------------------------------
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, UtilisateursListView, ArticlesListView, Moderateurs, ArticleDetailView,ModerateurDelete, ModerateursUpdate, ModerateursAdd, FavoriteArticleListView, SearchView,LocalUploadViewSet,ExternalUploadViewSet,SaveFavoriteView
#-----------------------------------------------------------------------------------------------

urlpatterns = [
    path('utilisateurs/', UtilisateursListView.as_view(), name='utilisateurs-list'),
    path('articles/', ArticlesListView.as_view(), name='articles-list'),
    path('articles/<str:article_id>/', ArticleDetailView.as_view(), name='article-detail'),
    #path('favoris/', FavorisListView.as_view(), name='favoris-list'),
    path('favoris/<int:user_id>/', FavoriteArticleListView.as_view(), name='user-favorite-articles'),
    path('search/', SearchView.as_view(), name='article_search'), 
    path('saveFavorite/', SaveFavoriteView.as_view(), name='save_favorite'),

    #--------------------------------------------------------------------------------------------------#
    #----------------------# ArticlesControl Views #---------------------------------------------------#
    #--------------------------------------------------------------------------------------------------#
    path('articles_ctrl/local-upload/', LocalUploadViewSet.as_view(), name='local-upload'), 
    path('articles_ctrl/external-upload/', ExternalUploadViewSet.as_view(), name='external-upload'),
    #--------------------------------------------------------------------------------------------------#
    path('login/', LoginView.as_view(), name='login'),
    #--------------------------------------------------------------------------------------------------#
    #----------------------# ModerateursControler  #---------------------------------------------------#
    #--------------------------------------------------------------------------------------------------#
    #Define URL paths for Moderateurs related views
    #Path to retrieve a list of moderators
    path('moderateurs/', Moderateurs.as_view(), name='moderateurs-list'),

    #Path to add a new moderator
    path('moderateurs/add', ModerateursAdd.as_view(), name='moderateurs-add'),

    #Path to update an existing moderator, requires an integer parameter 'id'
    path('moderateurs/update/<int:id>', ModerateursUpdate.as_view(), name='moderateurs-update'),

    #Path to delete an existing moderator, requires an integer parameter 'id'
    path('moderateurs/delete/<int:id>', ModerateurDelete.as_view(), name='moderateurs-delete'),

   ]



# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
