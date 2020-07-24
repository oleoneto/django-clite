from django import template

register = template.Library()


@register.filter
def {{ model }}(queryset):
    # code here...
    pass
