from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from movies.views import (
    ActorAPIViewSet,
    CountryAPIViewSet,
    GenreAPIViewSet,
    MovieAPIViewSet,
    AdminActorAPIViewSet,
    AdminCountryAPIViewSet,
    AdminGenreAPIViewSet,
    AdminMovieAPIViewSet
)

router = routers.DefaultRouter()
router.register("actors", ActorAPIViewSet, basename="actors")
router.register("countries", CountryAPIViewSet, basename="countries")
router.register("genres", GenreAPIViewSet, basename="genres")
router.register("movies", MovieAPIViewSet, basename="movies")
router.register("admin/actors", AdminActorAPIViewSet, basename="admin_actors")
router.register("admin/countries", AdminCountryAPIViewSet, basename="admin_countries")
router.register("admin/genres", AdminGenreAPIViewSet, basename="admin_genres")
router.register("admin/movies", AdminMovieAPIViewSet, basename="admin_movies")

urlpatterns = [
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("api/v1/", include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls')),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
