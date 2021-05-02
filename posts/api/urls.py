from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", views.index),
    path("comments", views.index2),
    path('create', views.create),
    path('addComment', views.addComment),
    path('like', views.like),
    path('delete/<int:id>', views.delete),
    path('unlike/<int:id>', views.unlike),
    path('update/<int:id>', views.update),
]
