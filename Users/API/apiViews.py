from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.API.serializer import UserSerializer, MessageSerializer, PostUsersSerializer, JoinedGroupsSerializer, CreatedGroupsSerializer, FriendsSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from Users.models import Message
from Users.models import Profile
from Users.models import Post, Friends, Message
import json
from django.db.models import Q
from posts.api.serializers import *
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

    friends = Friends.objects.filter(
        UID=request.user.id, status="Friends")

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


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def send_message(request, username):
    payload = json.loads(request.body)
    receiver = User.objects.get(username=username)

    print(payload["message"])
    print(request.user.username)
    print(receiver.username)

    message = Message.objects.create(
        senderID=request.user,
        receiverID=receiver,
        content=payload["message"]
    )
    print(message)
    serializer = MessageSerializer(message)
    return JsonResponse({'message': serializer.data}, safe=False, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_friend(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(poster_ID=user.id)
    createdGroups = Group.objects.filter(created_by=user.id)
    groups = join.objects.filter(UID=user.id)
    postsSerializer = PostSerializer(posts, many=True)
    createdGroupsSerializer = CreatedGroupsSerializer(createdGroups, many=True)
    groupsSerializer = JoinedGroupsSerializer(groups, many=True)

    friends = Friends.objects.filter(UID=user.id)
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
    recievedMessages = Message.objects.filter(
        senderID=request.user.id, receiverID=user.id)
    sentMessages = Message.objects.filter(
        senderID=user.id, receiverID=request.user.id)

    receiverID = request.user.id
    criterion1 = Q(senderID=request.user.id)
    criterion2 = Q(receiverID=user.id)
    criterion3 = Q(receiverID=request.user.id)
    criterion4 = Q(senderID=user.id)
    Messages = Message.objects.filter(
        criterion1 & criterion2 | criterion3 & criterion4).order_by('Time')

    Aserializer = MessageSerializer(Messages, many=True)
    # print(Aserializer.data)
    return JsonResponse({'Messages': Aserializer.data}, safe=False, status=status.HTTP_200_OK)


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


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_request(request, username):
    friend = User.objects.get(username=username)
    user = User.objects.get(id=request.user.id)
    newFriendRequest = Friends(UID=user, FID=friend, status="Pending")
    newFriendRequest.save()

    return JsonResponse({'Messages': "Success"}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def list_request(request):
    friends = Friends.objects.filter(
        UID=request.user.id, status="Pending")
    friendSerializer = FriendsSerializer(friends, many=True)

    return JsonResponse({'data': friendSerializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def reject_delete_request(request):
    username = request.data["friend"]
    friend = User.objects.get(username=username)
    user = User.objects.get(id=request.user.id)
    FriendInstance = Friends.objects.get(UID=user, FID=friend)
    FriendInstance.delete()
    return JsonResponse({'Messages': "Deleted Successfully"}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def accept_request(request):
    username = request.data["friend"]
    friend = User.objects.get(username=username)
    user = User.objects.get(id=request.user.id)
    FriendRequestInstance = Friends.objects.get(
        UID=user, FID=friend, status="Pending")

    FriendRequestInstance.status = "Friends"
    FriendRequestInstance.save()
    NewFriendRequest = Friends(UID=friend, FID=user, status="Friends")
    NewFriendRequest.save()

    return JsonResponse({'Messages': "Accepted Successfully"}, safe=False, status=status.HTTP_200_OK)


# add friend //Done
# reject add friend request //Done
# un friend //Done


# Khaled
# visit and show friends profile to see his data and its groups friends and posts and i can send him message or add request //Copy Paste
# send message to a friend //Straight
# i can reply on message


# edit profile data except gender and date of birth //Done
# show  all friends messages //Done
# admin can deactivate user  ???????????????
