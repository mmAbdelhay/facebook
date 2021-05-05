from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from django.db.models import Q
from groups.models import Group, join
from groups.api.serializers import GroupSerializer, JoinSerializer, UserSerializer
from Users.models import Post
from posts.api.serializers import PostSerializer
from django.contrib.auth.models import User


class IsGroupCreator(BasePermission):
    def has_permission(self, request, view):
        userId = request.user.id
        urlSplit = request.path.split("/")
        gid = int(urlSplit[len(urlSplit) - 1])
        gp = Group.objects.get(id=gid)
        creatorId = gp.created_by.id
        is_creator = (userId == creatorId)
        return is_creator


class IsGroupCreatorV2(BasePermission):
    def has_permission(self, request, view):
        userId = request.user.id
        gid = int(request.data["GID"])
        gp = Group.objects.get(id=gid)
        creatorId = gp.created_by.id
        is_creator = (userId == creatorId)
        return is_creator


class IsGroupCreatorV3(BasePermission):
    def has_permission(self, request, view):
        userId = request.user.id
        gid = int(request.query_params.get('gid', None))
        print(gid)
        gp = Group.objects.get(id=gid)
        creatorId = gp.created_by.id
        is_creator = (userId == creatorId)
        return is_creator


class IsMember(BasePermission):
    def has_permission(self, request, view):
        userId = request.user.id
        urlSplit = request.path.split("/")
        gid = int(urlSplit[len(urlSplit) - 1])
        gpMembers = join.objects.filter(GID=gid).filter(status='accepted').values_list('UID')
        gpMembersList = list(gpMembers)
        if userId in gpMembersList[0]:
            print("in if")
            return True
        return False


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def view_all_groups(request):
    users_id = join.objects.filter(UID=request.user.id).values_list('GID')
    print(users_id)
    print(request.user.id)
    all_group = Group.objects.exclude(id__in=users_id)
    print(all_group)
    serializer = GroupSerializer(instance=all_group, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, IsGroupCreator))
def view_all_pending_user(request, gid):
    users_id = join.objects.filter(GID=gid).filter(status='pending').values_list('UID')
    all_group_users = User.objects.filter(id__in=users_id)
    serializer = UserSerializer(instance=all_group_users, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def view_all_user_groups(request):
    user_group_id = join.objects.filter(UID=request.user.id).filter(status='accepted').values_list('GID')
    user_groups = Group.objects.filter(id__in=user_group_id.all())
    serializer = GroupSerializer(instance=user_groups, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def show(request, id):
    one_group = Group.objects.get(pk=id)
    users = join.objects.filter(Q(GID=id) & Q(status='accepted'))
    serializer = GroupSerializer(instance=one_group, many=False)
    joined = 0
    for item in users.iterator():
        if request.user.id == item.UID.id:
            joined = 1
            break
        else:
            joined = 0

    if joined == 1:
        posts = Post.objects.filter(group_ID=one_group.id)
        postSerializer = PostSerializer(instance=posts, many=True)
        GroupData = {
            'GroupData': serializer.data,
            'joined': joined,
            'postsData': postSerializer.data
        }
    else:
        GroupData = {
            'GroupData': serializer.data,
            'joined': joined,
        }
    return Response(data=GroupData, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):
    updatedRequest = request.data
    updatedRequest["created_by"] = request.user.id
    serializer = GroupSerializer(data=updatedRequest)
    if serializer.is_valid():
        serializer.save()
        CreatorUser = {
            "UID": request.user.id,
            "GID": serializer.data['id'],
            "status": "accepted"
        }
        serializer2 = JoinSerializer(data=CreatorUser)
        if serializer2.is_valid():
            serializer2.save()
        return Response(data={
            "success": True,
            "message": "group has been added successfully"
        }, status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, IsGroupCreatorV3))
def api_delete_user_from_group(request):
    uid = request.query_params.get('uid', None)
    gid = request.query_params.get('gid', None)
    try:
        customer = join.objects.filter(UID=uid, GID=gid)
    except join.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if len(customer) != 0:
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
@permission_classes((IsAuthenticated, IsGroupCreator))
def api_delete_group(request, gid):
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
@permission_classes((IsAuthenticated))
def get_all_group_posts(request, gid):  ######################## member
    allGroupPosts = Post.objects.filter(group_ID=gid).order_by('Time')
    serializer = PostSerializer(instance=allGroupPosts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def join_group_request(request):
    print(request.data)  # takes only GID in body
    updatedRequest = request.data
    print(updatedRequest)
    updatedRequest["UID"] = (request.user.id)
    print(updatedRequest)
    serializer = JoinSerializer(data=updatedRequest)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes((IsAuthenticated, IsGroupCreatorV2))
def approve_join_request(request, uid):
    updatedRequest = request.data
    updatedRequest["UID"] = (uid)
    updatedRequest["status"] = "accepted"

    oldJoin = join.objects.filter(UID=uid).get(GID=(updatedRequest["GID"]))

    print(updatedRequest)
    print(oldJoin)

    serializers = JoinSerializer(oldJoin, updatedRequest)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_posts_from_joined_groups(request, uid):
    user_group_id = join.objects.filter(UID=uid).filter(status='accepted').values_list('GID')
    print(user_group_id)
    allJoinedGroupsPosts = Post.objects.filter(group_ID__in=user_group_id).order_by('Time')
    print(allJoinedGroupsPosts)
    serializer = PostSerializer(instance=allJoinedGroupsPosts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all_users(request, gid):  ######################## member
    users_id = join.objects.filter(GID=gid).filter(status='accepted').values_list('UID')
    all_group_users = User.objects.filter(id__in=users_id)
    serializer = UserSerializer(instance=all_group_users, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_created_groups(request):  ######################## member
    user_id = request.user.id
    createdGroups = Group.objects.filter(created_by=user_id)
    serializer = GroupSerializer(instance=createdGroups, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
