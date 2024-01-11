from django.db import models
from django.contrib.auth.models import User

class UserAvatarModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
