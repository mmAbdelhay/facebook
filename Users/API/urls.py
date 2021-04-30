from django.urls import path
from . import apiViews
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("login", obtain_auth_token),
    path("signup", apiViews.api_signup),
]
