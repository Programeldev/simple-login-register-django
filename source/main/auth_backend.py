from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,
                     email=None, admin=False, **kwargs):
        if settings.USE_USERNAME:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

            if not admin and settings.USE_EMAIL and not user.email == email:
                return None
        else:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return None

        if not user.check_password(password):
            return None

        return user
