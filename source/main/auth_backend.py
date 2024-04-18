from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None,
                     password=None, email=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if not user.email == email:
            return None

        if not user.check_password(password):
            return None

        return user
