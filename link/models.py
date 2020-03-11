from django.contrib.auth.models import User
from django.db import models
import datetime

ACTIVE_STATUS = 0
DELETED_STATUS = 1


class LinkModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    identifier = models.CharField(unique=True, max_length=6)
    original_link = models.TextField(default='')
    status = models.IntegerField(choices=((ACTIVE_STATUS, 'active'), (DELETED_STATUS, 'deleted')), default=0)


class LinkVisitInfo(models.Model):
    link = models.ForeignKey(LinkModel, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now)
