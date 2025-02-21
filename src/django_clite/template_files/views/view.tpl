import datetime
from django.shortcuts import render
# from django.views.decorators.cache import cache_page
# from django.shortcuts import HttpResponse


# @cache_page(60 * 1)  # cache for 1 minute
def {{ name }}(request):
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
