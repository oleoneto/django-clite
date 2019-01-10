from jinja2 import Template


project_urls = Template("""
from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]
""")


app_urls = Template("""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
import rest_framework.authtoken.views as rf
from .views import *

router = routers.SimpleRouter(trailing_slash=False)
# router.register('model', ModelViewSet)

urlpatterns = [
    # Replace with your page name, the view class or method, and the name you'd
    # to use to resolve the url to this route.
    # path('/page', route, name='route'),
    
    
    # Django REST framework support
    # -- Add all API endpoints for the application
    # path('api/v1/', include(router.urls)),
    
    # -- Authentication route.
    # path('api/v1/auth/', include('rest_framework.urls')),
    
    # -- Request auth token for API access. Supports POST only.
    # path('api/v1/token/', rf.obtain_auth_token),
    
    # -- API documentation available with no login required
    # path('api/v1/docs/', include_docs_urls(title="{{ project }}", authentication_classes=[], permission_classes=[])),
]
""")
