from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

from jwt_auth.models import JWToken

import jwcrypto.jwk as jwk
import python_jwt as jwt


def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None
    return user


def auth_required(superuser_required):
    def wrapped1(func):
        def wrapped2(self, request, *args, **kwargs):
            token = request.META.get('HTTP_TOKEN', None)
            if token is None:
                raise PermissionDenied

            try:
                jwt_token = JWToken.objects.get(token=token)
            except JWToken.DoesNotExist:
                raise PermissionDenied
            else:
                try:
                    header, claims = jwt.verify_jwt(jwt_token.token, jwk.JWK.from_json(jwt_token.pub_key), ['RS256'])
                except jwt._JWTError:
                    raise PermissionDenied
                user_id = claims.get('user_id', None)
                if user_id is None:
                    raise PermissionDenied
                request.user = get_user(user_id)
                if not request.user or not request.user.is_superuser:
                    raise PermissionDenied
                return func(self, request, *args, **kwargs)
        return wrapped2
    return wrapped1
