from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from groups.models import Group,join
from groups.api.serializers import GroupSerializer,JoinSerializer


@api_view(['GET',])
def view_all_groups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(instance=groups, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def view_all_pending_user(request,gid):
    pending = join.objects.filter(GID=gid,status='pending')
    serializer = JoinSerializer(instance=pending, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET',])
def view_all_user_groups(request,uid):
    user_group_id = join.objects.filter(UID=uid).values_list('GID')
    user_groups = Group.objects.filter(id__in=user_group_id.all())
    serializer = GroupSerializer(instance=user_groups, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def show(request, id):
    one_group = Group.objects.get(pk=id)
    serializer = GroupSerializer(instance=one_group)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = GroupSerializer(data=request.data)

    if serializer.is_valid():
        group= serializer.save()
        print(type(request.user))
        group.created_by = request.user
        group.save()
        return Response(data={
            "success": True,
            "message": "group has been added successfully"
        }, status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_user_from_group(request):
    uid = request.query_params.get('uid', None)
    gid = request.query_params.get('gid', None)
    try:
        customer = join.objects.filter(UID=uid,GID=gid)
    except join.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if len(customer)!=0:
        operation = customer[0].delete()
        if operation:
            data = {"success": True}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {"success": False}
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        data = {"success": False, "error": {"code": 400, "message": "required parameters"}}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_group(request,gid):

    try:
        group = Group.objects.get(id=gid)
        group.delete()
        return Response(data={
            'message': 'deleted',
            'success': True
        }, status=status.HTTP_200_OK)

    except join.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
