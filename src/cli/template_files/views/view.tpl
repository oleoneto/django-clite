import datetime
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.urls import path
from {{ project }}.{{ app }}.url import urlpatterns
# from django.views.decorators.cache import cache_page


"""
Enable caching if needed. For example, to cache this view for 15 minutes, do:
@cache_page(60 * 15)
"""
def {{ name }}_view(request):
    template = '{{ name }}.html'
    context = {
        'date': datetime.datetime.now,
    }

    """
    Alternatively, your view can return HTML directly like so:
    html = '<html><body><h1>{{ classname }}View</h1>It is now %s.</body></html>' % date
    return HttpResponse(html)
    """
    return render(request, template, context)


urlpatterns.append(
    path('{{ name }}', {{ name }}_view, name='{{ name }}')
)
