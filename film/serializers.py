# movies/serializers.py
from rest_framework import serializers
from .models import Film, Video, Episode

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['file']

class EpisodeSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    
    class Meta:
        model = Episode
        fields = ['uuid', 'title', 'description', 'image', 'duration', 'video']

class FilmSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    episodes = EpisodeSerializer(many=True, read_only=True)
    category = serializers.CharField(source='type.nom', read_only=True)

    class Meta:
        model = Film
        fields = ['uuid', 'title', 'description', 'image', 'video', 'duration', 'category', 'episodes']

    def create(self, validated_data):
        video_data = validated_data.pop('video', None)
        film = Film.objects.create(**validated_data)
        if video_data:
            Video.objects.create(film=film, **video_data)
        return film