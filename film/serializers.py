# movies/serializers.py
from rest_framework import serializers
from .models import Film, Video, Episode, Type

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['uuid', 'nom']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['file']

class EpisodeSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    film = serializers.SlugRelatedField(queryset=Film.objects.all(), slug_field='uuid', required=False, allow_null=True)
    
    class Meta:
        model = Episode
        fields = ['uuid', 'title', 'description', 'image', 'duration', 'video', 'film']

class FilmSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    episodes = EpisodeSerializer(many=True, read_only=True)
    category = serializers.CharField(source='type.nom', read_only=True)
    type = serializers.SlugRelatedField(queryset=Type.objects.all(), slug_field='uuid', required=False, allow_null=True)

    class Meta:
        model = Film
        fields = ['uuid', 'title', 'description', 'image', 'video', 'duration', 'category', 'episodes', 'sortie_date', 'is_publier', 'type']

    def create(self, validated_data):
        video_data = validated_data.pop('video', None)
        film = Film.objects.create(**validated_data)
        if video_data:
            Video.objects.create(film=film, **video_data)
        return film