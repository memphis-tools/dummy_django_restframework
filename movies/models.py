from django.db import models

from . import validators


class Actor(models.Model):

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "actors"

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "countries"

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "genres"

    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name_plural = "movies"

    imdb_match = models.BooleanField("imdb match", default=False)
    title = models.CharField("movie title", max_length=125, unique=True)
    year = models.IntegerField("movie published year", validators=[validators.MustRespectDateRanges(), ])
    genres = models.ManyToManyField(Genre, related_name="movies")
    rating = models.FloatField("movie rating")
    description = models.CharField("movie description", max_length=1250)
    image = models.ImageField("movie picture", upload_to="media/", blank=True, null=True)
    actors = models.ManyToManyField(Actor, related_name="movies")
    director = models.CharField("movie director", max_length=250)
    writer = models.CharField("movie writer", max_length=250)
    trailer_url = models.URLField("movie trailer url", max_length=350)
    countries_of_origin = models.ManyToManyField(Country, related_name="movies")

    def __str__(self):
        return self.title
