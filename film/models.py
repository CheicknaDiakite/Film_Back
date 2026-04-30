# movies/models.py
from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class Type(models.Model):
    nom = models.CharField(max_length=100)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.nom

class Film(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies', null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(upload_to='images/')
    sortie_date = models.DateField(null=True, blank=True)

    is_publier = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE,null=True, blank=True, related_name='type')

    def __str__(self):
        return self.title

class Episode(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='episodes', null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    image = models.ImageField(upload_to='episodes/images/', null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.film.title} - {self.title}"

class Video(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    film = models.OneToOneField(Film, on_delete=models.CASCADE, related_name='video', null=True, blank=True)
    episode = models.OneToOneField(Episode, on_delete=models.CASCADE, related_name='video', null=True, blank=True)
    file = models.FileField(upload_to='videos/')

    def __str__(self):
        if self.film:
            return f"Vidéo (Film) - {self.film.title}"
        if self.episode:
            return f"Vidéo (Épisode) - {self.episode.title}"
        return "Vidéo"