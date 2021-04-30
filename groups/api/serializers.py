from rest_framework import serializers
from groups.models import Group


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
