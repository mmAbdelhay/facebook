from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from groups.models import Group
from groups.api.serializers import GroupSerializer


@api_view(['GET',])
def view_all_groups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(instance=groups, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
