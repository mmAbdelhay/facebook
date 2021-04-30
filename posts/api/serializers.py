from rest_framework import serializers
from Users.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def delete(self):
        id = self.data.get('id')
        post = Post.objects.get(pk=id)
        post.delete()
