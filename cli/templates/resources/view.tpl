import datetime
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.urls import path
from {{ project }}.{{ app }}.url import urlpatterns


"""
Enable caching if needed.
This page will be cached for 15 minutes.
@cache_page(60 * 15)
"""
def {{ name }}_view(request):
    template = "{{ name }}.html"
    context = {
        'date': datetime.datetime.now
    }

    """
    Alternatively, your view can return HTML directly like so:
    html = "<html><body><h1>{{ classname }}View</h1>It is now %s.</body></html>" % current_date
    return HttpResponse(html)
    """
    return render(request, template, context)


urlpatterns.append(
    path('{{ name }}', {{ name }}_view, name='{{ name }}')
)
