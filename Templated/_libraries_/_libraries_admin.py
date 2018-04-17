### Django-Autogenerator

"""
Admin Functions
Written by Leo Neto
Updated on April 14, 2018
"""

from django.contrib import admin

# _____________________________________________________
# Admin panel actions: Publish, Draft, Feature, Unfeature

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
    queryset.update(destaque=False)
make_unfeatured.short_description = "Unmark as featured content"
