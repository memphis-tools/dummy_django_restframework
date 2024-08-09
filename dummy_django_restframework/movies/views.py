from django.core.validators import validate_slug
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Actor, Country, Genre, Movie
from .permissions import IsAdminAuthenticated, IsStaffAuthenticated
from .serializers import (
    ActorDetailSerializer,
    ActorListSerializer,
    CountryDetailSerializer,
    CountryListSerializer,
    GenreDetailSerializer,
    GenreListSerializer,
    MovieDetailSerializer,
    MovieListSerializer,
)


class MultipleSerializerMixin:
    """A mixin to determinate the serializer to use for the view set"""
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["create", "retrieve", "update", "partial_update"] and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AdminActorAPIViewSet(MultipleSerializerMixin, ModelViewSet):
    """An admin viewset for Actor model"""
    serializer_class = ActorListSerializer
    detail_serializer_class = ActorDetailSerializer
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    def get_queryset(self):
        return Actor.objects.all()


class AdminCountryAPIViewSet(MultipleSerializerMixin, ModelViewSet):
    """An admin viewset for Country model"""
    serializer_class = CountryListSerializer
    detail_serializer_class = CountryDetailSerializer
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    def get_queryset(self):
        return Country.objects.all()


class AdminGenreAPIViewSet(MultipleSerializerMixin, ModelViewSet):
    """An admin viewset for Genre model"""
    serializer_class = GenreListSerializer
    detail_serializer_class = GenreDetailSerializer
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    def get_queryset(self):
        return Genre.objects.all()


class AdminMovieAPIViewSet(MultipleSerializerMixin, ModelViewSet):
    """An admin viewset for Movie model"""
    serializer_class = MovieListSerializer
    detail_serializer_class = MovieDetailSerializer
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    def get_queryset(self):
        return Movie.objects.all()


class ActorAPIViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    """An Actor model viewset"""
    serializer_class = ActorListSerializer
    detail_serializer_class = ActorDetailSerializer

    def get_queryset(self):
        queryset = Actor.objects.all()
        queryset = self.look_for_name(queryset)
        return queryset

    def look_for_name(self, queryset):
        name = self.request.GET.getlist("name")
        if name:
            queryset = queryset.filter(name__in=name)
        return queryset


class CountryAPIViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    """A Country model viewset"""
    serializer_class = CountryListSerializer
    detail_serializer_class = CountryDetailSerializer

    def get_queryset(self):
        name = self.request.GET.getlist("name")
        queryset = Country.objects.all()
        if name:
            queryset = queryset.filter(name__in=name)
        return queryset


class GenreAPIViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    """A Genre model viewset"""
    serializer_class = GenreListSerializer
    detail_serializer_class = GenreDetailSerializer

    def get_queryset(self):
        name = self.request.GET.getlist("name")
        queryset = Genre.objects.all()
        if name:
            queryset = queryset.filter(name__in=name)
        return queryset


class MovieAPIViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    """A Movie model viewset"""
    serializer_class = MovieListSerializer
    detail_serializer_class = MovieDetailSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        queryset = self.look_for_title(queryset)
        queryset = self.look_for_genre(queryset)
        queryset = self.look_for_actor(queryset)
        queryset = self.look_for_sort_by(queryset)
        queryset = self.look_for_page_size(queryset)
        return queryset

    def look_for_title(self, queryset):
        title = self.request.GET.get("title")
        if title:
            # the movie title is not case sensitive
            queryset = queryset.filter(title__iexact=title)
        return queryset

    def look_for_genre(self, queryset):
        genre_names = self.request.GET.getlist("genre")
        if genre_names:
            q_objects = Q()
            for genre in genre_names:
                try:
                    # a genre name can only contains letters, numbers, underscore or hyphens
                    validate_slug(genre)
                    # the genre name is not case sensitive
                    q_objects |= Q(agenre__name__iexact=genre)
                except ValidationError:
                    raise ValidationError(f"Invalid genre name {genre}")
            queryset = queryset.filter(genres__name__in=genre_names).distinct()
        return queryset

    def look_for_actor(self, queryset):
        actors = self.request.GET.getlist("actor")
        if actors:
            q_objects = Q()
            for actor in actors:
                # the actor name is not case sensitive
                q_objects |= Q(actors__name__iexact=actor)
            queryset = queryset.filter(q_objects).distinct()
        return queryset

    def look_for_sort_by(self, queryset):
        sort_by = self.request.GET.get("sort_by")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset

    def look_for_page_size(self, queryset):
        page_size = self.request.GET.get("page_size")
        if page_size:
            queryset = queryset[:int(page_size)]
        return queryset
