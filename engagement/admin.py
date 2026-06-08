from django.contrib import admin

from .models import (
    EpisodeComment,
    EpisodeLike,
    FilmComment,
    FilmLike,
    EpisodeFavorite,
    FilmFavorite,
)


@admin.register(FilmLike)
class FilmLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "film", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "film__title")


@admin.register(EpisodeLike)
class EpisodeLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "episode", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "episode__title", "episode__film__title")


@admin.register(FilmComment)
class FilmCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "film", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "film__title", "text")


@admin.register(EpisodeComment)
class EpisodeCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "episode", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "episode__title", "text")


@admin.register(FilmFavorite)
class FilmFavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "film", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "film__title")


@admin.register(EpisodeFavorite)
class EpisodeFavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "episode", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "episode__title", "episode__film__title")

