from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
# router.register(r'users', ProfileViewSet, basename='user_list'),
router.register(r'actors', ActorListViewSet, basename='actor_list'),
router.register(r'director', DirectorListViewSet, basename='director_list'),
router.register(r'genre', GenreViewSet, basename='genre_list'),
router.register(r'rating', RatingViewSet, basename='rating_list'),
router.register(r'favorite', FavoriteViewSet, basename='favorite_list'),
# router.register(r'country', CountryViewSet, basename='country_list'),

urlpatterns = [
    path('', include(router.urls)),
    path('movie/', MovieListAPIView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailAPIView.as_view(), name='movie_detail'),
    path('users/', ProfileListView.as_view(), name='user_list'),
    path('users/<int:pk>/', ProfileEditView.as_view(), name='user_detail'),
    path('country/', CountryListAPIView.as_view(), name='country_list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country_detail'),
]