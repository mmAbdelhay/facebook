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


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False, required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    def save(self, request):
        print(request.data)
        print(self.validated_data)
        userData = User(
            email=request.data.get('email'),
            username=request.data.get('username')
        )
        if request.data.get('password') != request.data.get('password2'):
            raise serializers.ValidationError({
                'password': 'passwords doesnt match'
            })
        else:
            userData.set_password(request.data.get('password'))
            userData.save()
            profile = Profile(
                gender=self.validated_data.get('gender'),
                birth_date=self.validated_data.get('birth_date'),
                user=userData,
                profileImg=self.validated_data.get('profileImg')
            )
            profile.save()


class MessageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='receiverID', read_only=True)

    class Meta:
        model = Message
        fields = ['name', 'Time', 'content']


class PostUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'Time', 'postImg', 'group_ID']


class JoinedGroupsSerializer(serializers.ModelSerializer):
    GroupName = serializers.CharField(source='GID', read_only=True)

    class Meta:
        model = join
        fields = ['GroupName', 'status', 'GID']


class CheckFriendsStatus(serializers.ModelSerializer):

    class Meta:
        model = Friends
        fields = ['status']


class FriendsSerializer(serializers.ModelSerializer):
    FriendName = serializers.CharField(source='UID', read_only=True)

    class Meta:
        model = Friends
        fields = ['FriendName', 'status']


class CreatedGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['created_at', 'overview', 'name', 'id']
