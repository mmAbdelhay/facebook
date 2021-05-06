from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.API.serializer import *
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
from posts.api.serializers import PostSerializer
from groups.models import join, Group
from django.core.exceptions import ObjectDoesNotExist


from django.core.mail import send_mail
from facebook.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives

@api_view(["POST"])
def api_signup(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(request)
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
        FID=request.user.id, status="Friends")

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
def get_users(request):
    responeDictionary = {}
    responeDictionary1 = []
    users = User.objects.all()
    for x in users:
        if (x.id != request.user.id) & (not (x.is_superuser)):
            print(x, x.id, x.username)
            responeDictionary['name'] = x.username
            friends = Friends.objects.filter(UID=x.id)
            friendSerializer = FriendsSerializer(friends, many=True)
            criterion1 = Q(UID=request.user.id)
            criterion2 = Q(FID=x.id)
            criterion3 = Q(FID=request.user.id)
            criterion4 = Q(UID=x.id)
            areTheyFriends = Friends.objects.filter(
                criterion1 & criterion2 | criterion3 & criterion4).count()

            if areTheyFriends == 0:
                responeDictionary['friends'] = "Strangers"
            elif areTheyFriends == 2:
                responeDictionary['friends'] = "Friends"
            else:
                areTheyFriends = Friends.objects.filter(
                    criterion1 & criterion2).count()
                if areTheyFriends == 1:
                    responeDictionary['friends'] = "Sent"
                else:
                    responeDictionary['friends'] = "Pending"

        print(not (responeDictionary in responeDictionary1))
        if bool(responeDictionary) & (not (responeDictionary in responeDictionary1)):
            responeDictionary_cp = responeDictionary.copy()
            print("hey: ", responeDictionary_cp)
            responeDictionary1.append(responeDictionary_cp)
            print("hello: ",responeDictionary1)






    return JsonResponse({'data': responeDictionary1}, safe=False, status=status.HTTP_200_OK)














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



    subject, from_email, to = 'new message', EMAIL_HOST_USER, receiver.email
    text_content = f"You have  received a new message from {request.user.username}"
    html_content = f'<div style="box-sizing: border-box;border: 1px solid #292929;width:50%;height: 200px;margin:auto;margin-top: 40px;"><div style="background-color: orangered;"><h2 style="padding: 10px;width: fit-content;margin: auto;color: white;">NEW MESSAGE NOTIFICATION :</h2></div><p style="width: fit-content;margin: auto;margin-top: 50px;">You have recieved a new message from {request.user.username} </p></div>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

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
    criterion1 = Q(UID=request.user.id)
    criterion2 = Q(FID=user.id)
    criterion3 = Q(FID=request.user.id)
    criterion4 = Q(UID=user.id)
    areTheyFriends = Friends.objects.filter(
        criterion1 & criterion2 | criterion3 & criterion4).count()
    responeDictionary = {}

    if areTheyFriends == 0:
        responeDictionary['friends'] = "Strangers"
    elif areTheyFriends == 2:
        responeDictionary['friends'] = "Friends"
    else:
        areTheyFriends = Friends.objects.filter(
            criterion1 & criterion2).count()
        if areTheyFriends == 1:
            responeDictionary['friends'] = "Sent"
        else:
            responeDictionary['friends'] = "Pending"

    responeDictionary['username'] = user.username
    responeDictionary['email'] = user.email
    responeDictionary['gender'] = user.profile.gender
    responeDictionary['birth_date'] = user.profile.birth_date
    responeDictionary['profileImg'] = str(user.profile.profileImg)
    # responeDictionary['friends'] = friendSerializer.data
    # for x in friendSerializer.data:
    #     if request.user.username == x['FriendName']:
    #         friends_status = x['status']
    #         break
    #     else:
    #         friends_status = 'not friends'

    # responeDictionary['friends_status'] = friends_status
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
        FID=request.user.id, status="Pending")
    friendSerializer = FriendsSerializer(friends, many=True)

    return JsonResponse({'data': friendSerializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def reject_delete_request(request):
    username = request.data["friend"]
    friend = User.objects.get(username=username)
    user = User.objects.get(id=request.user.id)
    # FriendInstance = Friends.objects.get(UID=user, FID=friend)
    if Friends.objects.filter(UID=user, FID=friend).exists():
        FriendInstance = Friends.objects.get(UID=user, FID=friend)
        FriendInstance.delete()
    if Friends.objects.filter(UID=friend, FID=user).exists():
        FriendInstance = Friends.objects.get(UID=friend, FID=user)
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
        FID=user, UID=friend, status="Pending")

    FriendRequestInstance.status = "Friends"
    FriendRequestInstance.save()
    NewFriendRequest = Friends(FID=friend, UID=user, status="Friends")
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
