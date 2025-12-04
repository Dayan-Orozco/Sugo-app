from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginUser(BaseBackend):
    def authenticate(self, request, country=None, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(country=country, phone=phone)
            # Validar el PIN encriptado
            if user.password and check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
