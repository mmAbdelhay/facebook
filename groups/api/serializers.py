from rest_framework import serializers
from groups.models import Group, join


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class JoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = join
        fields = "__all__"
