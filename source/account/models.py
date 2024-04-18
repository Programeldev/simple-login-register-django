from django.db import models
from django.contrib.auth.models import User

from .utils import avatar_path


class UserAvatarModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             primary_key=True)
    avatar = models.ImageField(upload_to=avatar_path)
