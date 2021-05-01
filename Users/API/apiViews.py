from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.API.serializer import UserSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from Users.models import Message


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
def get_conversation(request, username):
    # print(username)
    user = User.objects.get(username=username)
    messages = Message.objects.filter(
        senderID=request.user.id, receiverID=user.id)
    serializer = MessageSerializer(messages, many=True)
    # print(serializer.data)
    return JsonResponse({'Messages': serializer.data}, safe=False, status=status.HTTP_200_OK)
