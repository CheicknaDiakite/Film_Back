from django.urls import path

from . import views

urlpatterns = [
    path("films/<uuid:film_uuid>/engagement/", views.FilmEngagementView.as_view()),
    path("films/<uuid:film_uuid>/view/", views.FilmViewIncrementView.as_view()),
    path("films/<uuid:film_uuid>/like/", views.FilmLikeToggleView.as_view()),
    path("films/<uuid:film_uuid>/comments/", views.FilmCommentCreateView.as_view()),
    path("films/<uuid:film_uuid>/favorite/", views.FilmFavoriteToggleView.as_view()),
    path("episodes/<uuid:episode_uuid>/engagement/", views.EpisodeEngagementView.as_view()),
    path("episodes/<uuid:episode_uuid>/view/", views.EpisodeViewIncrementView.as_view()),
    path("episodes/<uuid:episode_uuid>/like/", views.EpisodeLikeToggleView.as_view()),
    path("episodes/<uuid:episode_uuid>/comments/", views.EpisodeCommentCreateView.as_view()),
    path("episodes/<uuid:episode_uuid>/favorite/", views.EpisodeFavoriteToggleView.as_view()),
    path("favorites/", views.UserFavoritesListView.as_view()),
]
