from django.urls import path
from groups.api.views import view_all_groups,show,create,api_delete_user_from_group,view_all_user_groups,api_delete_group,view_all_pending_user,get_all_group_posts,join_group_request,get_posts_from_joined_groups,approve_join_request,get_all_users,get_created_groups,view_all_user_requested_groups,api_delete_user_request_from_group

urlpatterns = [
    path("", view_all_groups,name= "all_groups"),
    path("<int:id>", show,name="one_group"),
    path('create', create,name="create_group"),
    path("delete/", api_delete_user_from_group),
    path("cancel/",api_delete_user_request_from_group),
    path("list/",view_all_user_groups),
    path("delete/<int:gid>",api_delete_group),
    path("pendings/<int:gid>",view_all_pending_user),
    path("posts/<int:gid>",get_all_group_posts),
    path("join",join_group_request),
    path("groupsposts/<int:uid>",get_posts_from_joined_groups),
    path("approve/<int:uid>",approve_join_request),
    path("users/<int:gid>",get_all_users),
    path("createdbyyou",get_created_groups),
    path("requested/",view_all_user_requested_groups),
]