from rest_framework import serializers
from Users.models import *
from django.contrib.auth.models import User
from groups.models import Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    UID = UserSerializer(read_only=True, many=False, required=False)

    class Meta:
        model = Comment
        # fields = "__all__"
        exclude = ('Time',)

    def save(self, id, request):
        bad_words = ['bitch', 'fuck', 'shit', 'piss', 'dick', 'asshole', 'bastard', 'cunt', 'damn']
        if any(x in request.data['content'] for x in bad_words):
            raise serializers.ValidationError({
                'error': 'content contains bad words'
            })
        else:
            comment = Comment(content=self.data['content'], UID=User.objects.get(pk=id),
                              postID=Post.objects.get(pk=self.data['postID']))
            comment.save()

    def delete(self):
        id = self.data.get('id')
        comment = Comment.objects.get(pk=id)
        comment.delete()


class LikesSerializer(serializers.ModelSerializer):
    UID = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Like
        fields = "__all__"

    def save(self, id):
        like = Like(UID=User.objects.get(pk=id), PID=Post.objects.get(pk=self.data['PID']))
        like.save()

    def unlike(self, like):
        like.delete()


class PostSerializer(serializers.ModelSerializer):
    post = CommentsSerializer(read_only=True, many=True)
    liked_post = LikesSerializer(read_only=True, many=True)
    poster_ID = UserSerializer(read_only=True, many=False)
    group_ID = GroupSerializer(read_only=True, many=False)

    class Meta:
        model = Post
        fields = '__all__'

    def save(self, id, request):
        bad_words = ['bitch', 'fuck', 'shit', 'piss', 'dick', 'asshole', 'bastard', 'cunt', 'damn', 'boobs',
                     'pussy', 'nipples']
        content = str(request.data['content'])
        if any(x in content.lower() for x in bad_words):
            raise serializers.ValidationError({
                'error': 'content contains bad words'
            })
        else:
            if 'group_ID' in request.data:
                try:
                    post = Post(content=request.data['content'], poster_ID=User.objects.get(pk=id),
                                group_ID=Group.objects.get(pk=request.data["group_ID"]), postImg=request.data['postImg'])
                    post.save()
                except:
                    post = Post(content=request.data['content'], poster_ID=User.objects.get(pk=id),
                                group_ID=Group.objects.get(pk=request.data["group_ID"]))

                    post.save()
            else:
                try:
                    post = Post(content=request.data['content'], poster_ID=User.objects.get(pk=id),
                                postImg=request.data['postImg'])
                    post.save()
                except:
                    post = Post(content=request.data['content'], poster_ID=User.objects.get(pk=id))
                    post.save()

    def delete(self):
        id = self.data.get('id')
        post = Post.objects.get(pk=id)
        post.delete()

    def update(self, content, post):
        post.content = content
        post.save()

class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('profileImg',)
