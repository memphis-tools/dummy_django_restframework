![Screenshot](https://img.shields.io/badge/python-v3.11-blue?logo=python&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/djangorestframework-v3.15.2-blue?logo=django&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/coveralls--blue?logo=coveralls&logoColor=yellow)
![pylint and flake](https://github.com/memphis-tools/dummy_django_restframework/actions/workflows/lint-flake.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/memphis-tools/dummy_django_restframework/badge.svg?branch=main)](https://coveralls.io/github/memphis-tools/dummy_django_restframework?branch=main)
![Known Vulnerabilities](https://snyk.io/test/github/memphis-tools/dummy_django_restframework/badge.svg)

# DUMMY APP FOR LEARNING PURPOSES

This dummy app takes advantage of a dummy MongoDB loaded as a submodule.

The database consists of random movies loaded from IMDb.

The project's aim is to provide a REST API using Django REST Framework, which then can be rendered on a Frontend.

Datas can be accessed without authentication.

## TECHNOLOGIES
Python 3.11 and later

Django Rest Framework

## HOW RUN IT ?

At the project root folder, touch (create) a ".env" file. Set something like this:

    export SECRET_KEY="88c06735211ca43cac81ab7385cdf61d35a5fd0aef43db9f3b8a384687433e56b9337855d7afefb7a18256432aa22c125c1c"
    export DEBUG=False
    export ADMIN_PASSWORD="SuperP@ssword"
    export DEFAULT_USER_PASSWORD="SuperP@ssword"
    export MONGO_SERVER="localhost"
    export MONGO_PORT="27017"
    export MONGO_DB="movies_db"
    export MONGO_INITDB_ROOT_USERNAME="admin"
    export MONGO_INITDB_ROOT_PASSWORD="SuperP@ssword"

  source .env

  git submodule update --remote

  python -m venv venv

  source venv/bin/activate

  pip install -r requirements.txt

  docker compose -f docker-compose.yml up -d --build

  python manage.py makemigrations

  python manage.py migrate

  python manage.py collectstatic

  python manage.py init_app

  python manage.py restore_dump_from_dummy_mongodb_movies

  python manage.py populate_django_movies_database

  python manage.py runserver

## TO RUN TESTS

  coverage run -m pytest

  coverage report

## HOW USE IT ?

The dummy Django REST Framework API will be served at: http://127.0.0.1:8000/api/v1/

The basic documentation is directly generated by drf_spectacular using default configuration. The docs can be consult:

  http://127.0.0.1:8000/api/v1/swagger/

  http://127.0.0.1:8000/api/v1/redoc/

  http://127.0.0.1:8000/api/v1/schema/

I have not fullfill the documentation. To synthesize it quickly. Read below.

  Movies can be displayed globally or individually.

    http://127.0.0.1:8000/api/v1/movies/

    http://127.0.0.1:8000/api/v1/movies/281
    
  Movies list can be filtered by title, actor(s), genre(s).

    http://127.0.0.1:8000/api/v1/movies/?title=12%20angry%20men

    http://127.0.0.1:8000/api/v1/movies/?actor=tom%20hanks

    http://127.0.0.1:8000/api/v1/movies/?actor=tom+hanks&actor=sylvester%20stallone

    http://127.0.0.1:8000/api/v1/movies/?genre=action

    http://127.0.0.1:8000/api/v1/movies/?genre=action&genre=romance


Only admin can create, update or delete actors, countries, genres or movies.

## USEFULL LINKS

Django REST Framework: https://www.django-rest-framework.org/

DRF Spectacular: https://drf-spectacular.readthedocs.io/en/latest/
