from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Film, Type, Episode
from .serializers import FilmSerializer, TypeSerializer, EpisodeSerializer

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

        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'