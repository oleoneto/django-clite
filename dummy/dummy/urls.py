"""dummy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
import rest_framework.authtoken.views as rf

from django.conf import settings
from django.conf.urls.static import static

from dummy.api.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register('artists', ArtistViewset)
router.register('albums', AlbumViewset)
router.register('tracks', TrackViewset)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('api-auth/', include_docs_urls('rest_framework.urls')),
    path('api-auth/token/', rf.obtain_auth_token),

    # No authentication required to view api documentation
    path('docs/', include_docs_urls(title="Dummy API", authentication_classes=[], permission_classes=[])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
