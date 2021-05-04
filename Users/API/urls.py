from django.urls import path
from . import apiViews
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("login", obtain_auth_token),
    path("signup", apiViews.api_signup),
    path("getMessages", apiViews.get_all_messages),
    path("getConversation/<str:username>", apiViews.get_conversation),
    path("getUser", apiViews.get_user),
    path("updateInfo", apiViews.update_Info),
    path("getUser/<str:username>", apiViews.get_friend),
    path("sendMessage/<str:username>", apiViews.send_message),

    path("addRequest/<str:username>", apiViews.add_request),
    path("ListRequests", apiViews.list_request),
    path("rejectRequest", apiViews.reject_delete_request),
    path("acceptRequest", apiViews.accept_request),


]

# "token": "532d33f021815898c4e7753a29842afa18792ecf"
