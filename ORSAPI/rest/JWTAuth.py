from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from service.models import User


class ServiceUserJWTAuthentication(JWTAuthentication):
    """JWT auth backend that resolves users from service.models.User instead of Django's auth.User."""

    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        if not user_id:
            raise InvalidToken("Token contains no user_id")
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
