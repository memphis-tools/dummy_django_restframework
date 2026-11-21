import os
import urllib.parse
from django.core.management.base import BaseCommand
from pymongo import MongoClient

from movies.models import Actor, Country, Genre, Movie


SOURCE_IMAGE_PATH = 'media/'


def import_mongodb_movies_into_django_db():
    # MongoDB connection settings
    mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    mongo_server = os.getenv("MONGO_SERVER")
    mongo_port = int(os.getenv("MONGO_PORT"))
    mongo_db = os.getenv("MONGO_DB")

    # URL encode username and password
    encoded_user = urllib.parse.quote_plus(mongo_user)
    encoded_password = urllib.parse.quote_plus(mongo_password)

    # Ensure that required environment variables are set
    if not (mongo_user and mongo_password and mongo_server and mongo_db):
        raise RuntimeError("MongoDB environment variables not properly set.")

    # MongoDB client setup
    client = MongoClient(
        f"mongodb://{encoded_user}:{encoded_password}@{mongo_server}:{mongo_port}/",
        uuidRepresentation="standard",
    )
    db = client[mongo_db]
    collection = db["movies"]
    mongodb_movies_list = list(collection.find({}))

    # mongodb_movies_list = list(mongodb_movies_list)
    total_movies = len(mongodb_movies_list)
    for index, movie in enumerate(mongodb_movies_list, start=1):
        movie.pop("_id")
        movie_image_name = movie.pop("image_name")
        movie_genres = movie.pop("genres")
        movie_actors = movie.pop("actors")
        movie_countries = movie.pop("countries_of_origin")

        # in the Movie viewset we want a genre displayed by name, not by id
        movie_genres_instances_list = []
        for genre in movie_genres:
            new_genre, created = Genre.objects.get_or_create(name=str(genre).lower())
            movie_genres_instances_list.append(new_genre)

        # in the Movie viewset we want an actor displayed by name, not by id
        movie_actors_list = []
        for actor in movie_actors:
            new_actor, created = Actor.objects.get_or_create(name=str(actor).lower())
            movie_actors_list.append(new_actor)

        # in the Movie viewset we want a country displayed by name, not by id
        movie_countries_list = []
        for country in movie_countries:
            new_country, created = Country.objects.get_or_create(name=str(country).lower())
            movie_countries_list.append(new_country)

        new_movie, _ = Movie.objects.get_or_create(**movie)

        for genre in movie_genres_instances_list:
            new_movie.genres.add(genre.id)

        for actor in movie_actors_list:
            new_movie.actors.add(actor)

        for country in movie_countries_list:
            new_movie.countries_of_origin.add(country)

        movie_image_file = os.path.join(SOURCE_IMAGE_PATH, movie_image_name)
        new_movie.image = movie_image_name
        new_movie.save()
        print(f"Saving movie: {index}/{total_movies}", end="\r")


class Command(BaseCommand):
    help = "Populate the Django project database through the submodule dummy_mongodb_imdb_movies"

    def handle(self, *args, **kwargs):
        import_mongodb_movies_into_django_db()
        self.stdout.write(self.style.SUCCESS("MongoDB movies imported Sir"))
