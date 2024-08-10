import os
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
import io
from PIL import Image

from movies.models import Actor, Country, Genre, Movie


@pytest.mark.django_db
class DummyApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="loulou",
            password=os.getenv("DEFAULT_USER_PASSWORD"),
            email="loulou@localhost"
        )
        cls.admin_user = User.objects.create_superuser(
            username="admin",
            password=os.getenv("DEFAULT_USER_PASSWORD"),
            email="admin@localhost"
        )
        cls.actor1 = Actor.objects.create(name="tom hanks")
        cls.actor2 = Actor.objects.create(name="toshiro mifume")
        cls.country1 = Country.objects.create(name="france")
        cls.country2 = Country.objects.create(name="germany")
        cls.country3 = Country.objects.create(name="japan")
        cls.genre1 = Genre.objects.create(name="thriller")
        cls.genre2 = Genre.objects.create(name="romance")
        cls.genre3 = Genre.objects.create(name="action")
        cls.movie1 = Movie.objects.create(
            title="No peace for heroes",
            year=2001,
            rating=9.1,
            description="In a cowardly world, the worst thing for heroes is not to fail, but to do nothing.",
            director=["akira kurosawa", ],
            writer=["akira kurosawa", ],
        )
        cls.movie1.genres.add(cls.genre2)
        cls.movie1.actors.add(cls.actor2)
        cls.movie1.countries_of_origin.add(cls.country3)

    @classmethod
    def get_dummy_image(cls):
        # Create an image in memory
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile("test_image.jpg", image_io.read(), content_type='image/jpeg')

    def tearDown(self):
        media_path = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_path):
            for file in files:
                if file.startswith("test_image"):
                    os.remove(os.path.join(root, file))


class TestActor(DummyApiTestCase):
    url = reverse_lazy("actors-list")

    def setUp(self):
        self.client.login(username="loulou", password=os.getenv("DEFAULT_USER_PASSWORD"))

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        admin_url = reverse_lazy("admin_actors-list")
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 200)

    def test_single_filtered_list(self):
        filtered_url = self.url + "?name=tom hanks"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'tom hanks')

    def test_multiple_filtered_list(self):
        filtered_url = self.url + "?name=tom hanks&name=toshiro mifume"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'tom hanks')
        self.assertEqual(response.data['results'][1]['name'], 'toshiro mifume')

    def test_create_with_user_viewset_without_authentication(self):
        actor_data = {"name": "mickey mouse"}
        response = self.client.post(self.url, data=actor_data)
        self.assertEqual(response.status_code, 405)

    def test_create_with_admin_viewset_without_authentication(self):
        self.client.logout()
        admin_url = reverse_lazy("admin_actors-list")
        actor_data = {"name": "mickey mouse"}
        response = self.client.post(admin_url, data=actor_data)
        self.assertEqual(response.status_code, 401)

    def test_create_with_admin_viewset_being_authenticated_as_user(self):
        admin_url = reverse_lazy("admin_actors-list")
        actor_data = {"name": "mickey mouse"}
        response = self.client.post(admin_url, data=actor_data)
        self.assertEqual(response.status_code, 403)

    def test_create_with_admin_viewset_being_authenticated_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        admin_url = reverse_lazy("admin_actors-list")
        actor_data = {"name": "mickey mouse"}
        response = self.client.post(admin_url, data=actor_data)
        self.assertEqual(response.status_code, 201)


class TestCountry(DummyApiTestCase):
    url = reverse_lazy("countries-list")

    def setUp(self):
        self.client.login(username="loulou", password=os.getenv("DEFAULT_USER_PASSWORD"))

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        admin_url = reverse_lazy("admin_countries-list")
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 200)

    def test_single_filtered_list(self):
        filtered_url = self.url + "?name=france"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'france')

    def test_multiple_filtered_list(self):
        filtered_url = self.url + "?name=france&name=germany"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'france')
        self.assertEqual(response.data['results'][1]['name'], 'germany')

    def test_create_with_user_viewset_without_authentication(self):
        country_data = {"name": "alaska"}
        response = self.client.post(self.url, data=country_data)
        self.assertEqual(response.status_code, 405)

    def test_create_with_admin_viewset_without_authentication(self):
        self.client.logout()
        admin_url = reverse_lazy("admin_countries-list")
        country_data = {"name": "alaska"}
        response = self.client.post(admin_url, data=country_data)
        self.assertEqual(response.status_code, 401)

    def test_create_with_admin_viewset_being_authenticated_as_user(self):
        admin_url = reverse_lazy("admin_countries-list")
        country_data = {"name": "alaska"}
        response = self.client.post(admin_url, data=country_data)
        self.assertEqual(response.status_code, 403)

    def test_create_with_admin_viewset_being_authenticated_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        admin_url = reverse_lazy("admin_countries-list")
        country_data = {"name": "alaska"}
        response = self.client.post(admin_url, data=country_data)
        self.assertEqual(response.status_code, 201)


class TestGenre(DummyApiTestCase):
    url = reverse_lazy("genres-list")

    def setUp(self):
        self.client.login(username="loulou", password=os.getenv("DEFAULT_USER_PASSWORD"))

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        admin_url = reverse_lazy("admin_genres-list")
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 200)

    def test_single_filtered_list(self):
        filtered_url = self.url + "?name=romance"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'romance')

    def test_multiple_filtered_list(self):
        filtered_url = self.url + "?name=thriller&name=romance"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'romance')
        self.assertEqual(response.data[1]['name'], 'thriller')

    def test_create_with_user_viewset_without_authentication(self):
        genre_data = {"name": "fantasy-romance"}
        response = self.client.post(self.url, data=genre_data)
        self.assertEqual(response.status_code, 405)

    def test_create_with_admin_viewset_without_authentication(self):
        self.client.logout()
        admin_url = reverse_lazy("admin_genres-list")
        genre_data = {"name": "fantasy-romance"}
        response = self.client.post(admin_url, data=genre_data)
        self.assertEqual(response.status_code, 401)

    def test_create_with_admin_viewset_being_authenticated_as_user(self):
        admin_url = reverse_lazy("admin_genres-list")
        genre_data = {"name": "fantasy-romance"}
        response = self.client.post(admin_url, data=genre_data)
        self.assertEqual(response.status_code, 403)

    def test_create_with_admin_viewset_being_authenticated_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        admin_url = reverse_lazy("admin_genres-list")
        genre_data = {"name": "fantasy-romance"}
        response = self.client.post(admin_url, data=genre_data)
        self.assertEqual(response.status_code, 201)


class TestMovie(DummyApiTestCase):
    url = reverse_lazy("movies-list")

    def setUp(self):
        self.client.login(username="loulou", password=os.getenv("DEFAULT_USER_PASSWORD"))

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        admin_url = reverse_lazy("admin_movies-list")
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 200)

    def test_single_filtered_list_with_title(self):
        filtered_url = self.url + "?title=No peace for heroes"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'No peace for heroes')

    def test_single_filtered_list_with_genre(self):
        filtered_url = self.url + "?genre=romance"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'No peace for heroes')

    def test_single_filtered_list_with_actor(self):
        filtered_url = self.url + "?actor=toshiro mifume"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'No peace for heroes')

    def test_create_with_user_viewset_without_authentication(self):
        movie_data = {}
        movie_data = movie_data
        response = self.client.post(self.url, data=movie_data)
        self.assertEqual(response.status_code, 405)

    def test_create_with_admin_viewset_without_authentication(self):
        self.client.logout()
        admin_url = reverse_lazy("admin_movies-list")
        movie_data = {}
        movie_data = movie_data
        response = self.client.post(admin_url, data=movie_data)
        self.assertEqual(response.status_code, 401)

    def test_create_with_admin_viewset_being_authenticated_as_user(self):
        admin_url = reverse_lazy("admin_movies-list")
        movie_data = {}
        movie_data = movie_data
        response = self.client.post(admin_url, data=movie_data)
        self.assertEqual(response.status_code, 403)

    def test_create_with_admin_viewset_being_authenticated_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        movie_data = {
            "title": "Yojimbo",
            "year": 1961,
            "rating": 9.5,
            "description": "A crafty ronin comes to a town divided by two criminal gangs.",
            "director": "akira kurosawa",
            "writer": "akira kurosawa",
            "genres": ["action"],
            "actors": ["toshiro mifume"],
            "countries_of_origin": ["japan"],
            "image": self.get_dummy_image(),
            "trailer_url": "https://dummy-things.com"
        }
        admin_url = reverse_lazy("admin_movies-list")
        movie_data = movie_data
        response = self.client.post(admin_url, data=movie_data)
        self.assertEqual(response.status_code, 201)

    def test_create_with_invalid_genre_being_authenticated_as_admin(self):
        self.client.logout()
        self.client.login(username="admin", password=os.getenv("DEFAULT_USER_PASSWORD"))
        movie_data = {
            "title": "Yojimbo",
            "year": 1961,
            "rating": 9.5,
            "description": "A crafty ronin comes to a town divided by two criminal gangs.",
            "director": "akira kurosawa",
            "writer": "akira kurosawa",
            "genres": ["fantasy"],
            "actors": ["toshiro mifume"],
            "countries_of_origin": ["japan"],
            "image": self.get_dummy_image(),
            "trailer_url": "https://dummy-things.com"
        }
        admin_url = reverse_lazy("admin_movies-list")
        movie_data = movie_data
        response = self.client.post(admin_url, data=movie_data)
        self.assertEqual(response.status_code, 400)
