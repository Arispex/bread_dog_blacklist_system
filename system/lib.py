from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from system.models import User


class AuthPasswordUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
