from django.contrib.auth.models import User
from django.db import models


class JWToken(models.Model):
    token = models.TextField(default='')
    pub_key = models.TextField(default='')
