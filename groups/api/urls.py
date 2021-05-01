from django.urls import path
from groups.api.views import view_all_groups,show,create,api_delete_user_from_group,view_all_user_groups,api_delete_group,view_all_pending_user

urlpatterns = [
    path("", view_all_groups,name= "all_groups"),
    path("<int:id>", show,name="one_group"),
    path('create', create,name="create_group"),
    path("delete/", api_delete_user_from_group),
    path("list/<int:uid>",view_all_user_groups),
    path("delete/<int:gid>",api_delete_group),
    path("pendings/<int:gid>",view_all_pending_user)
]