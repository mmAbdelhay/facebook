from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", views.index),
    path('create', views.create),
    path('delete/<int:id>', views.delete),
    path('update/<int:id>', views.update),
]
