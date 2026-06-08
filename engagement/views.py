from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from film.models import Episode, Film

from .models import EpisodeComment, EpisodeLike, FilmComment, FilmLike, EpisodeFavorite, FilmFavorite
from .serializers import EpisodeCommentSerializer, FilmCommentSerializer


class FilmEngagementView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, film_uuid):
        film = get_object_or_404(Film, uuid=film_uuid)
        like_count = FilmLike.objects.filter(film=film).count()
        liked_by_me = (
            request.user.is_authenticated
            and FilmLike.objects.filter(film=film, user=request.user).exists()
        )
        favorited_by_me = (
            request.user.is_authenticated
            and FilmFavorite.objects.filter(film=film, user=request.user).exists()
        )
        comments = (
            FilmComment.objects.filter(film=film)
            .select_related("user")
            .order_by("-created_at")[:200]
        )
        return Response(
            {
                "like_count": like_count,
                "liked_by_me": liked_by_me,
                "favorited_by_me": favorited_by_me,
                "comment_count": FilmComment.objects.filter(film=film).count(),
                "view_count": film.view_count,
                "comments": FilmCommentSerializer(comments, many=True).data,
            }
        )


class FilmViewIncrementView(APIView):
    """Incrémente le compteur de vues d'un film (appel typiquement une fois par session côté client)."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, film_uuid):
        film = get_object_or_404(Film, uuid=film_uuid)
        Film.objects.filter(pk=film.pk).update(view_count=F("view_count") + 1)
        film.refresh_from_db(fields=["view_count"])
        return Response({"view_count": film.view_count})


class FilmLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, film_uuid):
        film = get_object_or_404(Film, uuid=film_uuid)
        like, created = FilmLike.objects.get_or_create(film=film, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        like_count = FilmLike.objects.filter(film=film).count()
        return Response({"liked": liked, "like_count": like_count})


class FilmCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, film_uuid):
        film = get_object_or_404(Film, uuid=film_uuid)
        text = (request.data.get("text") or "").strip()
        if not text:
            return Response({"detail": "Le texte du commentaire est requis."}, status=status.HTTP_400_BAD_REQUEST)
        comment = FilmComment.objects.create(film=film, user=request.user, text=text)
        return Response(FilmCommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class EpisodeEngagementView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, episode_uuid):
        episode = get_object_or_404(Episode, uuid=episode_uuid)
        like_count = EpisodeLike.objects.filter(episode=episode).count()
        liked_by_me = (
            request.user.is_authenticated
            and EpisodeLike.objects.filter(episode=episode, user=request.user).exists()
        )
        favorited_by_me = (
            request.user.is_authenticated
            and EpisodeFavorite.objects.filter(episode=episode, user=request.user).exists()
        )
        comments = (
            EpisodeComment.objects.filter(episode=episode)
            .select_related("user")
            .order_by("-created_at")[:200]
        )
        return Response(
            {
                "like_count": like_count,
                "liked_by_me": liked_by_me,
                "favorited_by_me": favorited_by_me,
                "comment_count": EpisodeComment.objects.filter(episode=episode).count(),
                "view_count": episode.view_count,
                "comments": EpisodeCommentSerializer(comments, many=True).data,
            }
        )


class EpisodeViewIncrementView(APIView):
    """Incrémente le compteur de vues d'un épisode."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, episode_uuid):
        episode = get_object_or_404(Episode, uuid=episode_uuid)
        Episode.objects.filter(pk=episode.pk).update(view_count=F("view_count") + 1)
        episode.refresh_from_db(fields=["view_count"])
        return Response({"view_count": episode.view_count})


class EpisodeLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, episode_uuid):
        episode = get_object_or_404(Episode, uuid=episode_uuid)
        like, created = EpisodeLike.objects.get_or_create(episode=episode, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        like_count = EpisodeLike.objects.filter(episode=episode).count()
        return Response({"liked": liked, "like_count": like_count})


class EpisodeCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, episode_uuid):
        episode = get_object_or_404(Episode, uuid=episode_uuid)
        text = (request.data.get("text") or "").strip()
        if not text:
            return Response({"detail": "Le texte du commentaire est requis."}, status=status.HTTP_400_BAD_REQUEST)
        comment = EpisodeComment.objects.create(episode=episode, user=request.user, text=text)
        return Response(EpisodeCommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class FilmFavoriteToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, film_uuid):
        film = get_object_or_404(Film, uuid=film_uuid)
        favorite, created = FilmFavorite.objects.get_or_create(film=film, user=request.user)
        if not created:
            favorite.delete()
            favorited = False
        else:
            favorited = True
        return Response({"favorited": favorited})


class EpisodeFavoriteToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, episode_uuid):
        episode = get_object_or_404(Episode, uuid=episode_uuid)
        favorite, created = EpisodeFavorite.objects.get_or_create(episode=episode, user=request.user)
        if not created:
            favorite.delete()
            favorited = False
        else:
            favorited = True
        return Response({"favorited": favorited})


class UserFavoritesListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from film.serializers import FilmSerializer, EpisodeSerializer
        from film.models import Film, Episode

        favorite_films = Film.objects.filter(favorites__user=request.user)
        favorite_episodes = Episode.objects.filter(favorites__user=request.user)

        context = {"request": request}

        return Response({
            "films": FilmSerializer(favorite_films, many=True, context=context).data,
            "episodes": EpisodeSerializer(favorite_episodes, many=True, context=context).data
        })
