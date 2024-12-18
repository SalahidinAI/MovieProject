from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieListSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format('%Y'))
    genre = GenreSerializer(many=True)
    country = CountrySerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'year', 'genre', 'country', 'status_movie']


class MovieVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language', 'video']


class MovieMomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']


class RatingSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    user = ProfileSimpleSerializer()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'text', 'parent',
                  'stars', 'created_date']


class MovieDetailSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format('%d-%m-%Y'))
    director = DirectorListSerializer(many=True)
    actor = ActorListSerializer(many=True)
    genre = GenreSerializer(many=True)
    country = CountrySerializer(many=True)
    movie_videos = MovieVideosSerializer(many=True, read_only=True)
    movie_moments = MovieMomentsSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['movie_name', 'movie_image', 'movie_trailer', 'types',
                  'year', 'director', 'actor', 'genre', 'country',
                  'movie_time', 'description', 'status_movie', 'movie_moments', 'movie_videos',
                  'ratings']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class CountryDetailSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['country_name', 'movies']
