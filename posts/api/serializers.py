from rest_framework import serializers
from Users.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CommentsSerializer(serializers.ModelSerializer):
    UID = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Comment
        fields = "__all__"

class LikesSerializer(serializers.ModelSerializer):
    UID = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Like
        fields = "__all__"



class PostSerializer(serializers.ModelSerializer):
    post = CommentsSerializer(read_only=True, many=True)
    liked_post = LikesSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'
    def delete(self):
        id = self.data.get('id')
        post = Post.objects.get(pk=id)
        post.delete()
