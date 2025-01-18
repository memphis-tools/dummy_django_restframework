![Screenshot](https://img.shields.io/badge/python-v3.12.8-blue?logo=python&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/djangorestframework-v3.15.2-blue?logo=django&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/gunicorn-v22.0-blue?logo=gunicorn&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/postgresql-v15-blue?logo=postgresql&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/docker--blue?logo=docker&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/coveralls--blue?logo=coveralls&logoColor=yellow)
![pylint flake test](https://github.com/memphis-tools/dummy_django_restframework/actions/workflows/lint-flake-test.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/memphis-tools/dummy_django_restframework/badge.svg?branch=main)](https://coveralls.io/github/memphis-tools/dummy_django_restframework?branch=main)
![Known Vulnerabilities](https://snyk.io/test/github/memphis-tools/dummy_django_restframework/badge.svg)

# DUMMY APP FOR LEARNING PURPOSES

This dummy app takes advantage of a dummy MongoDB loaded as a submodule.

The database consists of random movies loaded from IMDb.

The MongoDB dump is already available with all needed datas.

The project's aim is to provide a REST API using Django REST Framework, which then can be rendered on a Frontend.

Datas can be accessed without authentication.

## TECHNOLOGIES
Python 3.12.8 and later

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
    export DEBUG=0
    export DJANGO_ALLOWED_HOSTS="192.168.1.5"
    export ADMIN_PASSWORD="super_p@ssword"
    export DEFAULT_USER_PASSWORD="super_p@ssword"
    export CORS_ALLOWED_ORIGINS="https://dummy-imdb-movies-frontend.dev:4443,https://localhost:4443"
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
    export DOCKER_HUB_USER="your_dockerhub_username"
    export DOCKER_HUB_PASSWORD="your_dockerhub_password_or_pat"

    source .env

We will simulate locally the https usage so we create a self signed certificate for Nginx:

    mkdir certs

    openssl req -x509 -nodes -days 3650 -newkey rsa:2049 -out certs/dummy-django-restframework.crt -keyout certs/dummy-django-restframework.key -subj "/CN=dummy-django-restframework.dev"

Optional: update your DNS entries, add self signed cert to your ca-trust.

Notice the CORS settings. **We are waiting for this hypothetic client**:

    CORS_ALLOWED_ORIGINS = [
        "https://dummy_imdb_movies_frontend.dev:4443",
        "https://localhost:4443",
    ]

We use nginx-unprivileged:alpine image. We check the nginx user ids and update the certs owner.

    docker run --rm nginxinc/nginx-unprivileged:alpine id nginx

    chown -R 101: certs

### RUN APP FOR THE FIRST TIME
We have 3 docker compose files:

  docker-compose-init.yml is used to initialize the DRF database with the MongoDB datas.

  docker-compose.yml is used once we have the Postgres database populated.

  docker-compose-test.yml is used during test, we do not use a reverse proxy.

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

Then you can reach the API: https://localhost/api/v1/movies/

So remember, once the application is initialized we do not need the MongoDB container anymore:

    docker compose -f docker-compose-init.yml down

    docker compose -f docker-compose.yml up -d

## TO RUN TESTS

    python -m venv venv

    source venv/bin/activate

    pip install -r dummy_django_restframework/requirements.txt

    source .env

    **export PYTHONPATH=$PYTHONPATH:./dummy_django_restframework**

    **export POSTGRES_HOST=localhost**

    **export IS_TESTING=True**

    docker compose -f docker-compose-test.yml up -d

    coverage run -m pytest

    coverage report

## HOW USE IT ?

The dummy Django REST Framework API will be served at: https://localhost/api/v1/

The basic documentation is directly generated by drf_spectacular using default configuration. The docs can be consult:

    https://localhost/api/v1/swagger/

    https://localhost/api/v1/redoc/

    https://localhost/api/v1/schema/

I have not fullfill the documentation. To synthesize it quickly. Read below.

  Movies can be displayed globally or individually.

    https://localhost/api/v1/movies/

    https://localhost/api/v1/movies/281

  Movies list can be filtered by title, actor(s), genre(s).

    https://localhost/api/v1/movies/?title=12%20angry%20men

    https://localhost/api/v1/movies/?actor=tom%20hanks

    https://localhost/api/v1/movies/?actor=tom+hanks&actor=sylvester%20stallone

    https://localhost/api/v1/movies/?genre=action

    https://localhost/api/v1/movies/?genre=action&genre=romance

Only admin can create, update or delete actors, countries, genres or movies.

## ABOUT PUBLISH NEW IMAGES

    docker build -t dummy_django_restframework:latest -f dummy_django_restframework/Dockerfile dummy_django_restframework/

    docker tag dummy_django_restframework:latest your_dockerhub_username/public_repo:dummy_django_restframework

    docker login -u your_dockerhub_username

    docker push your_dockerhub_username/public_repo:dummy_django_restframework

## USEFULL LINKS

Django REST Framework: https://www.django-rest-framework.org/

DRF Spectacular: https://drf-spectacular.readthedocs.io/en/latest/
