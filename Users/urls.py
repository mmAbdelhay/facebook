
from .API import apiViews
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('api/auth/', obtain_auth_token, name='api_token_auth'),
    # path('api/getbooks', apiViews.get_books),
    # path('api/addbook', apiViews.add_book),
    # path('api/<int:book_id>', apiViews.update_book),
    # path('api/del/<int:book_id>', apiViews.delete_book)


]
