# movies/serializers.py
from rest_framework import serializers
from .models import Film, Video, Episode, Type
from utilisateur.serializers import UserSerializer

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['uuid', 'nom']

class VideoSerializer(serializers.ModelSerializer):
    film_uuid = serializers.SlugRelatedField(source='film', queryset=Film.objects.all(), slug_field='uuid', required=False, allow_null=True)
    episode_uuid = serializers.SlugRelatedField(source='episode', queryset=Episode.objects.all(), slug_field='uuid', required=False, allow_null=True)
    
    class Meta:
        model = Video
        fields = ['uuid', 'file', 'film_uuid', 'episode_uuid']

    def validate(self, attrs):
        film = attrs.get('film')
        episode = attrs.get('episode')
        
        instance = self.instance
        
        if film:
            existing_video = Video.objects.filter(film=film)
            if instance:
                existing_video = existing_video.exclude(pk=instance.pk)
            if existing_video.exists():
                raise serializers.ValidationError({"film_uuid": "Ce film a déjà une vidéo associée."})
                
        if episode:
            existing_video = Video.objects.filter(episode=episode)
            if instance:
                existing_video = existing_video.exclude(pk=instance.pk)
            if existing_video.exists():
                raise serializers.ValidationError({"episode_uuid": "Cet épisode a déjà une vidéo associée."})
                
        return attrs

class EpisodeSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    film = serializers.SlugRelatedField(queryset=Film.objects.all(), slug_field='uuid', required=False, allow_null=True)
    video_file = serializers.FileField(write_only=True, required=False)
    
    class Meta:
        model = Episode
        fields = ['uuid', 'title', 'description', 'image', 'duration', 'video', 'film', 'video_file']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.film and instance.film.creator:
            data['creator'] = UserSerializer(instance.film.creator).data
        return data

    def create(self, validated_data):
        video_file = validated_data.pop('video_file', None)
        episode = Episode.objects.create(**validated_data)
        if video_file:
            Video.objects.create(episode=episode, file=video_file)
        return episode

    def update(self, instance, validated_data):
        video_file = validated_data.pop('video_file', None)
        instance = super().update(instance, validated_data)
        if video_file:
            video, created = Video.objects.get_or_create(episode=instance)
            video.file = video_file
            video.save()
        return instance

class FilmSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    episodes = EpisodeSerializer(many=True, read_only=True)
    category = serializers.CharField(source='type.nom', read_only=True)
    type = serializers.SlugRelatedField(queryset=Type.objects.all(), slug_field='uuid', required=False, allow_null=True)
    video_file = serializers.FileField(write_only=True, required=False)

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Film
        fields = ['uuid', 'title', 'description', 'image', 'video', 'duration', 'category', 'episodes', 'sortie_date', 'is_publier', 'type', 'video_file', 'creator']

    def create(self, validated_data):
        video_file = validated_data.pop('video_file', None)
        film = Film.objects.create(**validated_data)
        if video_file:
            Video.objects.create(film=film, file=video_file)
        return film

    def update(self, instance, validated_data):
        video_file = validated_data.pop('video_file', None)
        instance = super().update(instance, validated_data)
        if video_file:
            video, created = Video.objects.get_or_create(film=instance)
            video.file = video_file
            video.save()
        return instance