from django.urls import path, include
from rest_framework import routers
from .views import *
from .views import DirectorListAPIView

router = routers.SimpleRouter()
router.register(r'rating', RatingViewSet, basename='rating_list'),
router.register(r'favorite', FavoriteViewSet, basename='favorite_list'),
router.register(r'history', HistoryViewSet, basename='history_list'),

urlpatterns = [
    path('', include(router.urls)),
    path('movie/', MovieListAPIView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailAPIView.as_view(), name='movie_detail'),
    path('users/', ProfileListView.as_view(), name='user_list'),
    path('users/<int:pk>/', ProfileEditView.as_view(), name='user_detail'),
    path('country/', CountryListAPIView.as_view(), name='country_list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country_detail'),
    path('director/', DirectorListAPIView.as_view(), name='director_list'),
    path('director/<int:pk>/', DirectorDetailAPIView.as_view(), name='director_detail'),
    path('actor/', ActorListAPIView.as_view(), name='actor_list'),
    path('actor/<int:pk>/', ActorDetailAPIView.as_view(), name='actor_detail'),
    path('genre/', GenreListAPIView.as_view(), name='genre_list'),
    path('genre/<int:pk>/', GenreDetailAPIView.as_view(), name='genre_detail'),
]