from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.API.serializer import UserSerializer, MessageSerializer, PostSerializer, JoinedGroupsSerializer, CreatedGroupsSerializer, FriendsSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from Users.models import Message
from Users.models import Profile
from Users.models import Post, Friends
import json
from groups.models import join, Group
from django.core.exceptions import ObjectDoesNotExist


@api_view(["POST"])
def api_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success": True,
            "message": "user has been registered successfully"
        }, status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_all_messages(request):
    messages = Message.objects.filter(senderID=request.user.id)
    serializer = MessageSerializer(messages, many=True)
    # print()
    responeDictionary = {}
    for receiver in serializer.data:
        # print(receiver["content"])
        userObj = User.objects.filter(id=receiver["receiverID"])
        # print(userObj[0].username)
        responeDictionary[userObj[0].username] = receiver["content"]

    print(responeDictionary)
    return JsonResponse({'Messages': responeDictionary}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_user(request):
    user = User.objects.get(id=request.user.id)
    posts = Post.objects.filter(poster_ID=request.user.id)
    createdGroups = Group.objects.filter(created_by=request.user.id)
    groups = join.objects.filter(UID=request.user.id)
    postsSerializer = PostSerializer(posts, many=True)
    createdGroupsSerializer = CreatedGroupsSerializer(createdGroups, many=True)
    groupsSerializer = JoinedGroupsSerializer(groups, many=True)

    friends = Friends.objects.filter(UID=request.user.id)
    friendSerializer = FriendsSerializer(friends, many=True)

    responeDictionary = {}
    responeDictionary['username'] = user.username
    responeDictionary['email'] = user.email
    responeDictionary['gender'] = user.profile.gender
    responeDictionary['birth_date'] = user.profile.birth_date
    responeDictionary['profileImg'] = str(user.profile.profileImg)
    responeDictionary['friends'] = friendSerializer.data
    responeDictionary['posts'] = postsSerializer.data
    responeDictionary['createdGroups'] = createdGroupsSerializer.data
    responeDictionary['groups'] = groupsSerializer.data

    return JsonResponse({'data': responeDictionary}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_conversation(request, username):
    # print(username)
    user = User.objects.get(username=username)
    messages = Message.objects.filter(
        senderID=request.user.id, receiverID=user.id)
    serializer = MessageSerializer(messages, many=True)
    # print(serializer.data)
    return JsonResponse({'Messages': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_Info(request):
    payload = json.loads(request.body)
    try:
        user = User.objects.filter(id=request.user.id)
        user.update(**payload)
        return JsonResponse({'data': "Success"}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# add friend
# reject add friend request
# un friend


# Khaled
# visit and show friends profile to see his data and its groups friends and posts and i can send him message or add request //Copy Paste
# send message to a friend //Straight
# i can reply on message


# edit profile data except gender and date of birth //Done
# show  all friends messages //Done
# admin can deactivate user  ???????????????
