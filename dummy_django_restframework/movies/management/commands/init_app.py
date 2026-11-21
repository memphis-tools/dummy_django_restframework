import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from movies.models import Genre, Movie


SUPERUSER_NAME = "admin"
SUPERUSER_PASSWORD = os.getenv("ADMIN_PASSWORD")
SUPERUSER_EMAIL = "admin@localhost"


class Command(BaseCommand):
    help = "A dummy initialization"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users_list = [
            {
                "username": "donald",
                "first_name": "donald",
                "last_name": "duck",
                "password": os.getenv("DEFAULT_USER_PASSWORD"),
                "email": "donald.duck@bluelake.fr",
            },
            {
                "username": "daisy",
                "first_name": "daisy",
                "last_name": "duck",
                "password": os.getenv("DEFAULT_USER_PASSWORD"),
                "email": "daisy.duck@bluelake.fr",
            },
        ]

        current_users_size = User.objects.all().count()
        if current_users_size > 0:
            User.objects.all().delete()
            Movie.objects.all().delete()
            Genre.objects.all().delete()

        User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
        for new_user in users_list:
            User.objects.create_user(**new_user)

        self.stdout.write(self.style.SUCCESS("Django project database is initialized Sir"))
