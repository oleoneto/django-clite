from django.urls import path
from .views import *

# Replace the views and paths with your own views.
urlpatterns = [
    path('', homeView, name="home"),
    #path('create/', createView, name=create),
    #path('detail/', detailView, name=detail),
    #path('edit/', editView, name=edit),
]
