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


@api_view(["GET"])
def show(request, id):
    one_group = Group.objects.get(pk=id)
    serializer = GroupSerializer(instance=one_group)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create(request):
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success": True,
            "message": "group has been added successfully"
        }, status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)