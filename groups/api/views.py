from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from groups.models import Group,join
from groups.api.serializers import GroupSerializer,JoinSerializer
from Users.models import Post
from posts.api.serializers import PostSerializer

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def view_all_groups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(instance=groups, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def view_all_pending_user(request,gid):
    pending = join.objects.filter(GID=gid,status='pending')
    serializer = JoinSerializer(instance=pending, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def view_all_user_groups(request,uid):
    user_group_id = join.objects.filter(UID=uid).filter(status='accepted').values_list('GID') 
    user_groups = Group.objects.filter(id__in=user_group_id.all())
    serializer = GroupSerializer(instance=user_groups, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def show(request, id):
    one_group = Group.objects.get(pk=id)
    serializer = GroupSerializer(instance=one_group)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):
    updatedRequest=request.data
    updatedRequest["created_by"]=request.user.id
    serializer = GroupSerializer(data=updatedRequest)
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


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all_group_posts(request,gid):
    allGroupPosts=Post.objects.filter(group_ID=gid).order_by('Time')
    serializer = PostSerializer(instance=allGroupPosts,many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def join_group_request(request):    #takes only GID in body
    updatedRequest=request.data.dict()
    updatedRequest["UID"]=(request.user.id)
    serializer = JoinSerializer(data=updatedRequest)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def approve_join_request(request,uid):
    updatedRequest=request.data.dict()
    updatedRequest["UID"]=(uid)
    updatedRequest["status"]="accepted"

    oldJoin=join.objects.filter(UID=uid).get(GID=(updatedRequest["GID"]))

    print(updatedRequest)
    print(oldJoin)

    serializers = JoinSerializer(oldJoin,updatedRequest)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_posts_from_joined_groups(request,uid):
    user_group_id = join.objects.filter(UID=uid).filter(status='accepted').values_list('GID')
    print(user_group_id)
    allJoinedGroupsPosts=Post.objects.filter(group_ID__in=user_group_id).order_by('Time')
    print(allJoinedGroupsPosts)
    serializer = PostSerializer(instance=allJoinedGroupsPosts,many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
