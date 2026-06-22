from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.http import FileResponse, Http404
from django.utils.encoding import smart_str
import os
from .models import Film, Type, Episode, Video, Pub
from .serializers import FilmSerializer, TypeSerializer, EpisodeSerializer, VideoSerializer, PubSerializer
from .tasks import compress_video

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'
    
    def get_queryset(self):
        queryset = Video.objects.all()
        mine = self.request.query_params.get('mine')
        
        if mine == 'true' and self.request.user.is_authenticated:
            if self.request.user.role == 'creator':
                queryset = queryset.filter(
                    Q(film__creator=self.request.user) | 
                    Q(episode__film__creator=self.request.user)
                )
        return queryset

    def perform_create(self, serializer):
        """Sauvegarde la vidéo puis lance la compression en arrière-plan."""
        instance = serializer.save()
        compress_video.delay(instance.pk)

    def perform_update(self, serializer):
        """Lance la compression uniquement si un nouveau fichier est fourni."""
        instance = serializer.save()
        if 'file' in self.request.FILES:
            # Réinitialiser le statut avant de relancer la compression
            instance.compression_status = 'pending'
            instance.save(update_fields=['compression_status'])
            compress_video.delay(instance.pk)

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, uuid=None):
        """
        Stream the video file as an attachment so the browser triggers a download.
        GET /api/videos/<uuid>/download/
        """
        video = self.get_object()
        if not video.file:
            raise Http404("Aucun fichier vidéo trouvé.")

        file_path = video.file.path
        if not os.path.exists(file_path):
            raise Http404("Le fichier vidéo est introuvable sur le serveur.")

        # Build a friendly filename: <title>.<ext>
        ext = os.path.splitext(file_path)[1]  # e.g. '.mp4'
        if video.film:
            friendly_name = f"{video.film.title}{ext}"
        elif video.episode:
            friendly_name = f"{video.episode.film.title} - {video.episode.title}{ext}"
        else:
            friendly_name = os.path.basename(file_path)

        response = FileResponse(
            open(file_path, 'rb'),
            content_type='video/mp4',
            as_attachment=True,
            filename=smart_str(friendly_name),
        )
        return response

class TypeViewSet(viewsets.ModelViewSet):
    serializer_class = TypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 'type' is the related_name for films in the Film model
        if instance.type.exists():
            return Response(
                {"error": "Impossible de supprimer cette catégorie car elle est liée à des films ou épisodes existants."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Type.objects.all()
        
        # Only filter for 'list' action and if 'all=true' is not provided
        if self.action == 'list' and self.request.query_params.get('all') != 'true':
            from django.db.models import Count
            queryset = queryset.annotate(film_count=Count('type')).filter(film_count__gt=0)
            
        return queryset

class FilmViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = Film.objects.all()
        q = self.request.query_params.get('q')
        type_uuid = self.request.query_params.get('type')
        latest = self.request.query_params.get('latest')
        mine = self.request.query_params.get('mine')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(episodes__title__icontains=q) |
                Q(episodes__description__icontains=q)
            ).distinct()
        
        if type_uuid:
            queryset = queryset.filter(type__uuid=type_uuid)
        
        if latest:
            queryset = queryset.order_by('-created_at')

        if mine == 'true' and self.request.user.is_authenticated:
            if self.request.user.role == 'creator':
                queryset = queryset.filter(creator=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = Episode.objects.all()
        mine = self.request.query_params.get('mine')

        if mine == 'true' and self.request.user.is_authenticated:
            if self.request.user.role == 'creator':
                queryset = queryset.filter(film__creator=self.request.user)
        
        return queryset


class PubViewSet(viewsets.ModelViewSet):
    serializer_class = PubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = Pub.objects.all()
        is_publier = self.request.query_params.get('is_publier')
        if is_publier == 'true':
            queryset = queryset.filter(is_publier=True)
        elif is_publier == 'false':
            queryset = queryset.filter(is_publier=False)
        return queryset