from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from Users.models import Post, Comment, Like
from groups.models import *
from posts.api.serializers import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def index(request):
    try:
        friends = Friends.objects.filter(UID=request.user.id)
        groups = join.objects.filter(UID=request.user.id).filter(status='accepted')
        print('try1')
    except:
        try:

            friends = Friends.objects.get(UID=request.user.id)
            print('try2')
        except:
            friends = None
        try:

            groups = join.objects.filter(UID=request.user.id).filter(status='accepted')
            print('try3')
        except:
            groups = None

    try:
            print('1')
            g= []
            f= []
            print('===')
            for items in friends.iterator():
                f.append(items.FID)
                print(items.FID)
                print('===')

            for item in groups.iterator():
                g.append(item.GID)
                print(item.GID)

            posts = Post.objects.filter(
                Q(poster_ID=request.user.id) | Q(poster_ID__in=f) | Q(group_ID__in=g))
    except:
        try:
            print('2')
            g = []
            for item in groups.iterator():
                g.append(item.GID)
                print(item.GID)

            posts = Post.objects.filter(Q(poster_ID=request.user.id) | Q(group_ID__in=g))
        except:
            try:
                print('3')
                posts = Post.objects.filter(Q(poster_ID=request.user.id) | Q(poster_ID__in=friends.FID))
            except:
                try:
                    print('4')
                    posts = Post.objects.filter(poster_ID=request.user.id)
                except:
                    return Response(data={
                        "success": True,
                        "message": "Error in loading data"
                    }, status=status.HTTP_400_BAD_REQUEST)

    serializer = PostSerializer(instance=posts, many=True)
    for item in serializer.data:
        for like in item['liked_post']:
            try:
                profile = Profile.objects.get(user=like['UID']['id'])
                profileSerializer = ProfileSerializer(instance=profile)
                like['UID']['profileImg']=profileSerializer.data['profileImg']
                # print(like['UID']['profileImg'])
                if like['UID']['id'] == request.user.id :
                   item ['liked'] = 1
            except:
                print("error")


        for like in item['post']:
            try:
                profile = Profile.objects.get(user=like['UID']['id'])
                profileSerializer = ProfileSerializer(instance=profile)
                like['UID']['profileImg']=profileSerializer.data['profileImg']
            except:
                print('error')
         # like in item['poster_ID']:
        try:
            profile = Profile.objects.get(user=item['poster_ID']['id'])
            profileSerializer = ProfileSerializer(instance=profile)
            item['poster_ID']['profileImg']=profileSerializer.data['profileImg']
        except:
            print('error')

        #     print(like)
        #     print (getattr(like, 'username'))
        #     # profile = Profile.objects.get(user=like)
        #     # profileSerializer = ProfileSerializer(instance=profile)
        #     # like['profileImg']=profileSerializer.data['profileImg']




    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyPosts(request):
    posts = Post.objects.filter(poster_ID=request.user.id)
    serializer = PostSerializer(instance=posts, many=True)
    for item in serializer.data:
        for like in item['liked_post']:
            try:
                profile = Profile.objects.get(user=like['UID']['id'])
                profileSerializer = ProfileSerializer(instance=profile)
                like['UID']['profileImg'] = profileSerializer.data['profileImg']
                # print(like['UID']['profileImg'])
                if like['UID']['id'] == request.user.id:
                    item['liked'] = 1
            except:
                print("error")

        for like in item['post']:
            try:
                profile = Profile.objects.get(user=like['UID']['id'])
                profileSerializer = ProfileSerializer(instance=profile)
                like['UID']['profileImg'] = profileSerializer.data['profileImg']
            except:
                print('error')
        # like in item['poster_ID']:
        try:
            profile = Profile.objects.get(user=item['poster_ID']['id'])
            profileSerializer = ProfileSerializer(instance=profile)
            item['poster_ID']['profileImg'] = profileSerializer.data['profileImg']
        except:
            print('error')
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def gitPostsByName(request,name):
    user = User.objects.get(username=name)
    posts = Post.objects.filter(poster_ID=user.id).filter(group_ID__isnull=True)
    serializer = PostSerializer(instance=posts, many=True)
    for item in serializer.data:
        for like in item['liked_post']:
            try:
                profile = Profile.objects.get(user=like['UID']['id'])
                profileSerializer = ProfileSerializer(instance=profile)
                like['UID']['profileImg'] = profileSerializer.data['profileImg']
                # print(like['UID']['profileImg'])
                if like['UID']['id'] == request.user.id:
                    item['liked'] = 1
            except:
                print("error")

        for like in item['post']:
            try:
                profile = Profile.objects.get(user=like['UID']['id'])
                profileSerializer = ProfileSerializer(instance=profile)
                like['UID']['profileImg'] = profileSerializer.data['profileImg']
            except:
                print('error')
        # like in item['poster_ID']:
        try:
            profile = Profile.objects.get(user=item['poster_ID']['id'])
            profileSerializer = ProfileSerializer(instance=profile)
            item['poster_ID']['profileImg'] = profileSerializer.data['profileImg']
        except:
            print('error')
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def index2(request):
    posts = Comment.objects.all()
    serializer = CommentsSerializer(instance=posts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = PostSerializer(data=request.data)
    # print(request.user.id);
    if serializer.is_valid():
        serializer.save(request.user.id, request)
        return Response(data={
            "success": True,
            "message": "post has been added successfully"
        }, status=status.HTTP_201_CREATED)

    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addComment(request):
    serializer = CommentsSerializer(many=False, data=request.data)
    if serializer.is_valid():
        serializer.save(request.user.id)
        return Response(data={
            'message': 'comment added',
            'success': True
        }, status=status.HTTP_201_CREATED)
    return Response(data={
        'Error': serializer.errors,
        'success': False
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like(request):
    serializer = LikesSerializer(many=False, data=request.data)
    if serializer.is_valid():
        serializer.save(request.user.id)
        return Response(data={
            'message': 'you liked the post successfully',
            'success': True
        }, status=status.HTTP_201_CREATED)
    return Response(data={
        'Error': serializer.errors,
        'success': False
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike(request, id):
    # print(like)
    try:
        like = Like.objects.get(UID=request.user.id, PID=id)
        print(like)
        serializer = LikesSerializer(instance=like, many=False)
        if request.user.id == like.UID.id:
            serializer.unlike(like)
            return Response(data={
                'message': 'unliked',
                'success': True
            }, status=status.HTTP_200_OK)
        else:
            return Response(data={
                'Error': 'not owner',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(data={
            'Error': 'not liked',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, id):
    post = Post.objects.get(pk=id)
    serializer = PostSerializer(instance=post, many=False)
    if request.user.id == post.poster_ID.id:
        serializer.delete()
        return Response(data={
            'message': 'deleted',
            'success': True
        }, status=status.HTTP_200_OK)
    else:
        return Response(data={
            'Error': 'not owner',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteComment(request, id):
    comment = Comment.objects.get(pk=id)
    serializer = CommentsSerializer(instance=comment, many=False)
    print(comment.UID.id)
    print(request.user.id)
    if request.user.id == comment.UID.id :
        serializer.delete()
        return Response(data={
            'message': 'deleted',
            'success': True
        }, status=status.HTTP_200_OK)
    else:
        return Response(data={
            'Error': 'not owner',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request, id):
    post = Post.objects.get(pk=id)
    serializer = PostSerializer(instance=post, many=False, data=request.data)
    if serializer.is_valid():
        if request.user.id == post.poster_ID.id:
            serializer.update(request.data['content'], post)
            return Response(data={
                'message': 'post updated',
                'success': True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'Error': 'not owner',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={
        'Error': serializer.errors,
        'success': False
    }, status=status.HTTP_400_BAD_REQUEST)