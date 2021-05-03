from rest_framework import serializers
from Users.models import *
from django.contrib.auth.models import User
from groups.models import Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')


class CommentsSerializer(serializers.ModelSerializer):
    UID = UserSerializer(read_only=True, many=False, required=False)

    class Meta:
        model = Comment
        # fields = "__all__"
        exclude = ('Time',)

    def save(self, id):
            comment = Comment(content=self.data['content'], UID=User.objects.get(pk=id), postID=Post.objects.get(pk=self.data['postID']))
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

    def unlike(self,like):
        like.delete()


class PostSerializer(serializers.ModelSerializer):
    post = CommentsSerializer(read_only=True, many=True)
    liked_post = LikesSerializer(read_only=True, many=True)
    poster_ID = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Post
        fields = '__all__'

    def save(self, id):
            if self.data['group_ID']:
                try:
                 post = Post(content=self.data['content'], poster_ID=User.objects.get(pk=id),group_ID=Group.objects.get(pk=self.data["group_ID"]),postImg=self.data['postImg'])
                 post.save()
                except:
                    post = Post(content=self.data['content'], poster_ID=User.objects.get(pk=id),
                                group_ID=Group.objects.get(pk=self.data["group_ID"]))

                    post.save()
            else :
                try:
                    post = Post(content=self.data['content'], poster_ID=User.objects.get(pk=id),postImg=self.data['postImg'])
                    post.save()
                except:
                    post = Post(content=self.data['content'], poster_ID=User.objects.get(pk=id))
                    post.save()


    def delete(self):
        id = self.data.get('id')
        post = Post.objects.get(pk=id)
        post.delete()

    def update(self,content,post):
            post.content=content
            post.save()
