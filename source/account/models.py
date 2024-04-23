from pathlib import Path

from django.db import models
from django.contrib.auth.models import User


def avatar_path(instance, filename):
    avatar_name = '{}_avatar_{}'.format(instance.user.id, filename)
    path = Path(
        '/'.join((
            str(Path(instance.avatar.path).parent),
            avatar_name
        ))
    )
    path.unlink(missing_ok=True)

    return '{}_avatar_{}'.format(instance.user.id, filename)


class UserAvatarModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             primary_key=True)
    avatar = models.ImageField(upload_to=avatar_path)
