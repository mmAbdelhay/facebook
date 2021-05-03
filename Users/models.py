from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from groups.models import Group


class Profile(models.Model):
    def __str__(self):
        return str(self.user)

    MALE = 'M'
    FEMALE = 'F'
    Gender = (
        (MALE, 'M'),
        (FEMALE, 'F'),
    )
    gender = models.CharField(
        max_length=2,
        choices=Gender,
        default=MALE,
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    # profileImg = models.ImageField()
    profileImg = models.ImageField(upload_to='images/', null=True, blank=True)


class Post(models.Model):
    def __str__(self):
        return str(self.content)

    poster_ID = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField(max_length=1024)
    Time = models.DateField(auto_now_add=True)
    postImg = models.ImageField(blank=True, null=True)
    group_ID = models.ForeignKey(
        Group, blank=True, on_delete=models.CASCADE, null=True)


class Message(models.Model):
    class Meta:
        unique_together = (('senderID', 'receiverID', 'Time'),)

    senderID = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='sender')
    receiverID = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='receiver')
    Time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1024)


class Friends(models.Model):
    class Meta:
        unique_together = (('UID', 'FID'),)

    UID = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                            related_name='main_User')
    FID = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                            related_name='friend')

    Pending = 'Pending'
    Accepted = 'Friends'
    Status = (
        (Pending, 'Pending'),
        (Accepted, 'Friends'),
    )
    status = models.CharField(
        max_length=15,
        choices=Status
    )


class Like(models.Model):
    class Meta:
        unique_together = (('UID', 'PID'),)

    UID = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                            related_name='likerID')
    PID = models.ForeignKey(Post, on_delete=models.CASCADE,
                            related_name='liked_post')


class Comment(models.Model):
    # class Meta:
    #     unique_together = (('UID', 'postID', 'Time'),)
    UID = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='commenter')
    postID = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post')
    Time = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=1024)
