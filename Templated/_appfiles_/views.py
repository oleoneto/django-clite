### Django-Autogenerator

from _libraries_views import *
from .models import *
from .forms import *
from .serializers import *

# A test view which returns an template and two context variables.
def homeView(request):
    # Replace with your own model object.
    #instances = ModelName.objects.all()
    number = 100
    context = {
        'page': 'homeView',
        'number': 'number',
        #'instances': instances,
    }
    return render(request, '_sample_/home.html', context)


def aboutView(request):
    context = {
        'page': 'aboutView',
    }
    return render(request, '_sample_/about.html', context)
