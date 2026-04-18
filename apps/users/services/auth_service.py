from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def login_user(email, password):
    user = authenticate(email=email, password=password)

    if not user:
        raise AuthenticationFailed("Invalid credentials")

    refresh = RefreshToken.for_user(user)

    return {
        "user": user,
        "tokens": {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
    }