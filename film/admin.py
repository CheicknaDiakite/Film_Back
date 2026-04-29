from django.contrib import admin
from .models import Type, Film, Episode, Video

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

class VideoInline(admin.StackedInline):
    model = Video
    can_delete = True
    fk_name = 'film'
    extra = 1

class EpisodeInline(admin.StackedInline):
    model = Episode
    fk_name = 'film'
    extra = 1

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):

    pass

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):

    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    
    pass
