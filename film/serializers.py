# movies/serializers.py
from rest_framework import serializers
from .models import Film, Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['file']

class FilmSerializer(serializers.ModelSerializer):
    video = VideoSerializer()

    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'image', 'video']

    def create(self, validated_data):
        video_data = validated_data.pop('video')
        film = Film.objects.create(**validated_data)
        Video.objects.create(film=film, **video_data)
        return film