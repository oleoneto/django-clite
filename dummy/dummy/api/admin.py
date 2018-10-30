from django.contrib import admin
from .models import *

# Django-autogenerator

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark elements as published"

def make_draft(modeladmin, request, queryset):
    queryset.update(status='d')
make_draft.short_description = "Mark elements as draft"

def make_featured(modeladmin, request, queryset):
    queryset.update(featured=True)
make_featured.short_description = "Mark as featured content"

def make_unfeatured(modeladmin, request, queryset):
    queryset.update(featured=False)
make_unfeatured.short_description = "Unmark as featured content"

class TracksInline(admin.TabularInline):
    model = Track

class AlbumInline(admin.TabularInline):
    model = Album

class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumInline]

class AlbumAdmin(admin.ModelAdmin):
    inlines = [TracksInline]
    list_display = ['title', 'artist']

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ArtistReview)
admin.site.register(AlbumReview)
admin.site.register(TrackReview)
