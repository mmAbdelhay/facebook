from django.urls import path
from groups.api.views import view_all_groups,show,create

urlpatterns = [
    path("", view_all_groups,name= "all_groups"),
    path("<int:id>", show,name="one_group"),
    path('create', create,name="create_group"),
    #path("delete/<int:id>", views.destroy),
]