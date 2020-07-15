import datetime
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.urls import path
from .routes import routes


"""
Enable caching if needed.
This page will be cached for 15 minutes.
@cache_page(60 * 15)
"""
def {{ model.lower() }}_view(request):
    template = "{{ model.lower() }}.html"
    current_date = datetime.datetime.now()
    context = {
        'date': current_date
    }

    """
    Alternatively, your view can return HTML directly like so:
    html = "<html><body><h1>{{ classname }}View</h1>It is now %s.</body></html>" % current_date
    return HttpResponse(html)
    """
    return render(request, template, context)


routes.append(
    path('{{ view_name }}', {{ model.lower() }}_view, name='{{ view_name }}')
)
