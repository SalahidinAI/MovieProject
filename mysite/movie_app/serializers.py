from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile # в начале это строка должна быть User чтобы не возникла ошибка
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)  # в начале это строка должна быть User. вместо UserProfile. чтобы не возникла ошибка
        return user

    def to_representation(self, instance): # если эту функцию написать то мы будем получать новый токен при каждом регистрации
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):  # если эту функцию написать то мы будем получать новый токен при каждом логине
        refresh = RefreshToken.for_user(instance)
        return {
            'user': { #  это можно не писать и тогда мы увидем только токены, но для удобства их оставим
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


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


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieListSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format('%Y'))
    genre = GenreListSerializer(many=True)
    country = CountrySerializer(many=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'year', 'genre',
                  'country', 'status_movie', 'avg_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()


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
    genre = GenreListSerializer(many=True)
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
    user = ProfileSimpleSerializer()
    movie = MovieListSerializer()

    class Meta:
        model = History
        fields = ['user', 'movie', 'viewed_at']


class CountryDetailSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['country_name', 'movies']


class DirectorDetailSerializer(serializers.ModelSerializer):
    director_movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Director
        fields = ['director_name', 'director_image', 'bio', 'age', 'director_movies']


class ActorDetailSerializer(serializers.ModelSerializer):
    actor_movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['actor_name', 'actor_image', 'bio', 'age', 'actor_movies']


class GenreDetailSerializer(serializers.ModelSerializer):
    genre_movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['genre_name', 'genre_movies']

