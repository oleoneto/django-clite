from django import template

register = template.Library()


@register.filter
def {{ name }}(queryset):
    pass
