from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import datetime

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
