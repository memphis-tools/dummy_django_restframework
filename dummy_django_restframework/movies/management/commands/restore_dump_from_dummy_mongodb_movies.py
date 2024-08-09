import os
from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "Restore a MongoDB database dump from the submodule dummy_mongodb_imdb_movies's container."

    def handle(self, *args, **kwargs):
        try:
            copy_dump_command = [
                "sudo",
                "docker",
                "cp",
                "dummy_mongodb_imdb_movies/app/db_dump",
                "dummy_mongodb_movies:/data/db/dump"
            ]
            subprocess.run(
                copy_dump_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.stdout.write(self.style.SUCCESS("MongoDB dump copied, Sir"))
            admin_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
            admin_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
            restore_dump_command = [
                "sudo",
                "docker",
                "exec",
                "dummy_mongodb_movies",
                "mongorestore",
                "--db",
                "movies_db",
                "/data/db/dump/movies_db",
                "--username", admin_username,
                "--password", admin_password,
                "--authenticationDatabase", "admin"
            ]
            subprocess.run(
                restore_dump_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.stdout.write(self.style.SUCCESS("MongoDB dump restored, Sir"))

            unarchive_movies_pictures = [
                "tar",
                "-C",
                "dummy_mongodb_imdb_movies/",
                "-xzf",
                "dummy_mongodb_imdb_movies/app/movies_pictures/movies_pictures.tar.gz"
            ]
            subprocess.run(
                unarchive_movies_pictures,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.stdout.write(self.style.SUCCESS("Movies pictures unarchived, Sir"))

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Error running command: {e.stderr.decode('utf-8')}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Docker or Docker Compose is not installed or not found in PATH"))
