from rest_framework import serializers

from utilisateur.serializers import UserSerializer

from .models import EpisodeComment, FilmComment


class FilmCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FilmComment
        fields = ["id", "user", "text", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class EpisodeCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EpisodeComment
        fields = ["id", "user", "text", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
