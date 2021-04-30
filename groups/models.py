from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class join(models.Model):
    class Meta:
        unique_together = (('UID', 'GID'),)
    UID = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                            related_name='User')
    GID = models.ForeignKey(Group, on_delete=models.DO_NOTHING,
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
