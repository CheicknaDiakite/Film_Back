# movies/views.py
from rest_framework import viewsets, permissions
from .models import Film
from .serializers import FilmSerializer

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)