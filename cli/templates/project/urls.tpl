from django.urls import path, include
import rest_framework.authtoken.views as rf

handler400 = 'rest_framework.exceptions.bad_request'
handler500 = 'rest_framework.exceptions.server_error'

urlpatterns = [
    path('auth/token', rf.obtain_auth_token),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('v1/', include('project.example.api', namespace='example_api')),
]