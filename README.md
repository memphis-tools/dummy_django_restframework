![Screenshot](https://img.shields.io/badge/python-v3.11-blue?logo=python&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/djangorestframework-v3.15.2-blue?logo=django&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/gunicorn-v22.0-blue?logo=gunicorn&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/postgresql-v15-blue?logo=postgresql&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/docker--blue?logo=docker&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/coveralls--blue?logo=coveralls&logoColor=yellow)
<<<<<<< Updated upstream
![pylint and flake](https://github.com/memphis-tools/dummy_django_restframework/actions/workflows/lint-flake.yml/badge.svg)
=======
![pylint flake test](https://github.com/memphis-tools/dummy_django_restframework/actions/workflows/lint-flake-test.yml/badge.svg)
>>>>>>> Stashed changes
[![Coverage Status](https://coveralls.io/repos/github/memphis-tools/dummy_django_restframework/badge.svg?branch=main)](https://coveralls.io/github/memphis-tools/dummy_django_restframework?branch=main)
![Known Vulnerabilities](https://snyk.io/test/github/memphis-tools/dummy_django_restframework/badge.svg)

# DUMMY APP FOR LEARNING PURPOSES

This dummy app takes advantage of a dummy MongoDB loaded as a submodule.

The database consists of random movies loaded from IMDb.

The MongoDB dump is already available with all needed datas.

The project's aim is to provide a REST API using Django REST Framework, which then can be rendered on a Frontend.

Datas can be accessed without authentication.

## TECHNOLOGIES
Python 3.11 and later

Django Rest Framework

Docker

Postgresql

## HOW RUN IT ?

### PREREQUISITES
First we clone the repository:

    git clone --recurse-submodules https://github.com/memphis-tools/dummy_django_restframework.git

    cd dummy_django_restframework

    git submodule update --remote

At the project root folder, touch (create) a ".env" file. Set something like this:

    export SECRET_KEY="super_secret_key"
    export DEBUG=False
    export DJANGO_ALLOWED_HOSTS="192.168.1.5"
    export ADMIN_PASSWORD="super_p@ssword"
    export DEFAULT_USER_PASSWORD="super_p@ssword"
    export MONGO_SERVER="dummy_mongodb_movies"
    export MONGO_PORT="27017"
    export MONGO_DB="movies_db"
    export MONGO_INITDB_ROOT_USERNAME="admin"
    export MONGO_INITDB_ROOT_PASSWORD="super_p@ssword"
    export POSTGRES_USER=postgres
    export POSTGRES_PASSWORD="super_p@ssword"
    export POSTGRES_DB="movies_db"
    export POSTGRES_PORT="5432"
    export POSTGRES_HOST="db"
    export POSTGRES_ENGINE=django.db.backends.postgresql
    export DOCKER_HUB_USER="your_dockerhub_username"
    export DOCKER_HUB_PASSWORD="your_dockerhub_password_or_pat"

  source .env

### RUN APP FOR THE FIRST TIME
We have 2 docker compose files:

  docker-compose-init.yml is used to initialize the DRF database with the MongoDB datas. Also used for tests.

  docker-compose.yml is used once we have the Postgres database populated.

As several steps are involved for initialization, no entrypoint is made.

  docker compose -f docker-compose-init.yml up -d

**we copy the MongoDB dump**

    docker cp dummy_mongodb_imdb_movies/app/db_dump dummy_mongodb_movies:/data/db/dump

**we restore the dump**

    docker exec dummy_mongodb_movies mongorestore --db movies_db /data/db/dump/dump/movies_db --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin

**we copy images**

    docker cp dummy_mongodb_imdb_movies/app/movie_picture/no_image_available.jpg django_drf:/home/dummy-operator/web/media/

    docker cp dummy_mongodb_imdb_movies/app/movies_pictures/movies_pictures.tar.gz django_drf:/home/dummy-operator/web/media/

    docker exec django_drf tar -C /home/dummy-operator/web/media/ --strip-components=2 -xvf /home/dummy-operator/web/media/movies_pictures.tar.gz

**we initialize application**

    docker compose -f docker-compose.yml exec django_drf python manage.py makemigrations movies --noinput

    docker compose -f docker-compose.yml exec django_drf python manage.py migrate --noinput

    docker compose -f docker-compose.yml exec django_drf python manage.py collectstatic --no-input --clear

    docker compose -f docker-compose.yml exec django_drf python manage.py init_app

    docker compose -f docker-compose.yml exec django_drf python manage.py populate_django_movies_database

Then you can reach the API: http://0.0.0.0/api/v1/

So remember, once the application is initialized we do not need the MongoDB container anymore:

    docker compose -f docker-compose-init.yml down

    docker compose -f docker-compose.yml up

## TO RUN TESTS

    python -m venv venv

    source venv/bin/activate

    pip install -r requirements.txt

    source .env

    docker compose -f docker-compose-init.yml up -d

    export PYTHONPATH=$PYTHONPATH:./dummy_django_restframework

    export POSTGRES_HOST=localhost

    coverage run -m pytest

    coverage report

## HOW USE IT ?

The dummy Django REST Framework API will be served at: http://0.0.0.0/api/v1/

The basic documentation is directly generated by drf_spectacular using default configuration. The docs can be consult:

    http://0.0.0.0/api/v1/swagger/

    http://0.0.0.0/api/v1/redoc/

    http://0.0.0.0/api/v1/schema/

I have not fullfill the documentation. To synthesize it quickly. Read below.

  Movies can be displayed globally or individually.

    http://0.0.0.0/api/v1/movies/

    http://0.0.0.0/api/v1/movies/281

  Movies list can be filtered by title, actor(s), genre(s).

    http://0.0.0.0/api/v1/movies/?title=12%20angry%20men

    http://0.0.0.0/api/v1/movies/?actor=tom%20hanks

    http://0.0.0.0/api/v1/movies/?actor=tom+hanks&actor=sylvester%20stallone

    http://0.0.0.0/api/v1/movies/?genre=action

    http://0.0.0.0/api/v1/movies/?genre=action&genre=romance

Only admin can create, update or delete actors, countries, genres or movies.

## USEFULL LINKS

Django REST Framework: https://www.django-rest-framework.org/

DRF Spectacular: https://drf-spectacular.readthedocs.io/en/latest/
