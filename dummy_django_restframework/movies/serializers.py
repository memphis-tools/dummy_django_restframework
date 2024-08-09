from PIL import Image
from typing import List
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    ImageField,
    SlugRelatedField
)

from .models import Actor, Country, Genre, Movie


class ActorDetailSerializer(ModelSerializer):
    """A detail serializer for Actor model"""
    movies = SerializerMethodField()

    class Meta:
        model = Actor
        fields = ["id", "name", "movies"]

    def get_movies(self, instance) -> List[str]:
        return [movie.title for movie in instance.movies.all()]


class ActorListSerializer(ModelSerializer):
    """A list serializer for Actor model"""
    nb_movies = SerializerMethodField()

    class Meta:
        model = Actor
        fields = ["id", "name", "nb_movies"]

    def get_nb_movies(self, instance) -> int:
        return instance.movies.count()


class CountryDetailSerializer(ModelSerializer):
    """A detail serializer for Country model"""
    movies = SerializerMethodField()

    class Meta:
        model = Country
        fields = ["id", "name", "movies"]

    def get_movies(self, instance) -> List[str]:
        return [movie.title for movie in instance.movies.all()]


class CountryListSerializer(ModelSerializer):
    """A list serializer for Country model"""
    nb_movies = SerializerMethodField()

    class Meta:
        model = Country
        fields = ["id", "name", "nb_movies"]

    def get_nb_movies(self, instance) -> int:
        return instance.movies.count()


class GenreDetailSerializer(ModelSerializer):
    """A detail serializer for Genre model"""
    movies = SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["id", "name", "movies"]

    def get_movies(self, instance) -> List[str]:
        return [movie.title for movie in instance.movies.all()]


class GenreListSerializer(ModelSerializer):
    """A list serializer for Actor model"""
    nb_movies = SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["id", "name", "nb_movies"]

    def get_nb_movies(self, instance) -> int:
        return instance.movies.count()


class MovieDetailSerializer(ModelSerializer):
    """A detail serializer for Movie model"""
    genres = SlugRelatedField(
        slug_field="name",
        queryset=Genre.objects.all(),
        many=True
    )
    actors = SlugRelatedField(
        slug_field="name",
        queryset=Actor.objects.all(),
        many=True
    )
    countries_of_origin = SlugRelatedField(
        slug_field="name",
        queryset=Country.objects.all(),
        many=True
    )

    image = ImageField(max_length=125, allow_empty_file=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "genres",
            "rating",
            "image",
            "year",
            "description",
            "actors",
            "director",
            "writer",
            "countries_of_origin",
            "trailer_url"
        ]

    def validate_image(self, value):
        if value:
            if not value.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise ValidationError("File must be a .jpg, .jpeg, or .png image.")
            if value.size > 2 * 1024 * 1024:
                raise ValidationError("File size must not exceed 2 MB.")
            # Check file content
            try:
                image = Image.open(value)
                # Verify that fileis an image
                image.verify()
            except (IOError, SyntaxError):
                raise ValidationError("File content is not a valid image.")
        return value

    def get_actors(self, instance) -> List[str]:
        return [actor.name for actor in instance.actors.all()]

    def get_countries_of_origin(self, instance) -> List[str]:
        return [country.name for country in instance.countries_of_origin.all()]


class MovieListSerializer(ModelSerializer):
    """A list serializer for Actor model"""
    genres = SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "genres",
            "rating",
            "image",
            "year",
            "description",
            "trailer_url"
        ]

    def get_genres(self, instance) -> List[str]:
        return [genre.name for genre in instance.genres.all()]

    def validate_title(self, data):
        if Movie.objects.filter(title=data):
            raise ValidationError("Titre existe déjà")
        return data
