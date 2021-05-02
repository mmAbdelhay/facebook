from rest_framework import serializers
from django.contrib.auth.models import User
from Users.models import Message, Profile, Post, Friends
from groups.models import join, Group


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", 'email', "password", "password2"]

    def save(self, **kwargs):
        user = User(
            email=self.validated_data.get('email'),
            username=self.validated_data.get('username')
        )
        if self.validated_data.get('password') != self.validated_data.get('password2'):
            raise serializers.ValidationError({
                'password': 'passwords doesnt match'
            })
        else:
            user.set_password(self.validated_data.get('password'))
            user.save()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiverID', 'Time', 'content']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'Time', 'postImg', 'group_ID']


class JoinedGroupsSerializer(serializers.ModelSerializer):
    GroupName = serializers.CharField(source='GID', read_only=True)

    class Meta:
        model = join
        fields = ['GroupName', 'status']


class FriendsSerializer(serializers.ModelSerializer):
    FriendName = serializers.CharField(source='FID', read_only=True)

    class Meta:
        model = Friends
        fields = ['FriendName']


class CreatedGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['created_at', 'overview', 'name']
