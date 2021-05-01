from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    overview = models.TextField(max_length=1024)
    number_of_members = models.IntegerField(blank=True,null=True)
    name = models.TextField(max_length=20)


class join(models.Model):
    class Meta:
        unique_together = (('UID', 'GID'),)
    UID = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                            related_name='User')
    GID = models.ForeignKey(Group, on_delete=models.CASCADE,
                            related_name='Group')
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'
    joining_status = (
        (pending, 'pending'),
        (accepted, 'accepted'),
        (rejected, 'rejected')
    )
    status = models.CharField(
        max_length=100,
        choices=joining_status,
        default=pending,
    )


# Create your models here.
