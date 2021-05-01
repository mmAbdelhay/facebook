from django.urls import path
from groups.api.views import view_all_groups

urlpatterns = [
    path("", view_all_groups,name= "all_groups"),
  #  path('create', views.create),
  #  path('delete/<int:id>', views.delete),
   # path('update/<int:id>', views.update),
]