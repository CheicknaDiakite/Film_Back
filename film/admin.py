from django.contrib import admin
from .models import Type, Film, Episode, Video

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'uuid')
    search_fields = ('nom',)
    readonly_fields = ('uuid',)

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
    list_display = ('title', 'type', 'is_publier', 'created_at', 'uuid')
    list_filter = ('type', 'is_publier')
    search_fields = ('title', 'description')
    readonly_fields = ('uuid',)
    inlines = [VideoInline, EpisodeInline]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'film', 'duration', 'uuid')
    list_filter = ('film',)
    search_fields = ('title', 'description')
    readonly_fields = ('uuid',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'file', 'film', 'episode')
    readonly_fields = ('uuid',)
