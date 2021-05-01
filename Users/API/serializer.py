from rest_framework import serializers
from django.contrib.auth.models import User
from Users.models import Message, Profile


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



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user.username','gender', 'birth_date', 'profileImg']