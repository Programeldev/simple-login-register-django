from django.apps import AppConfig
from django.db.models.signals import post_delete


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        from .models import UserAvatarModel
        from .signals import delete_avatar

        post_delete.connect(delete_avatar, sender=UserAvatarModel)
