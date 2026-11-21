from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "Create and run a MongoDB container from the submodule dummy_mongodb_imdb_movies"

    def handle(self, *args, **kwargs):
        try:
            command = ["docker", "compose", "-f", "dummy_mongodb_imdb_movies/docker-compose.yml", "up", "-d"]
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.stdout.write(self.style.SUCCESS("MongoDB container is running Sir"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Error running command: {e.stderr.decode('utf-8')}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Docker or Docker Compose is not installed or not found in PATH"))
