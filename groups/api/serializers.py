from rest_framework import serializers
from groups.models import Group, join
from django.contrib.auth.models import User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class JoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = join
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =["id","username", 'email']
