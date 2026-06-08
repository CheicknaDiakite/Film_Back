from django.conf import settings
from django.db import models

from film.models import Episode, Film

User = settings.AUTH_USER_MODEL


class FilmLike(models.Model):
    """Un utilisateur ne peut liker un film qu'une seule fois."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="film_likes")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "film"],
                name="engagement_filmlike_unique_user_film",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} → {self.film}"


class EpisodeLike(models.Model):
    """Un utilisateur ne peut liker un épisode qu'une seule fois."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="episode_likes")
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "episode"],
                name="engagement_episodelike_unique_user_episode",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} → {self.episode}"


class FilmComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="film_comments")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Commentaire de {self.user} sur {self.film}"


class EpisodeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="episode_comments")
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Commentaire de {self.user} sur {self.episode}"


class FilmFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="film_favorites")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "film"],
                name="engagement_filmfavorite_unique_user_film",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} ★ {self.film}"


class EpisodeFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="episode_favorites")
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "episode"],
                name="engagement_episodefavorite_unique_user_episode",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} ★ {self.episode}"

