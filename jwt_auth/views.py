# Serializers define the API representation.

import datetime

import jwcrypto.jwk as jwk
import python_jwt as jwt
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics
from .models import JWToken
from . import serializers


# ViewSets define the view behavior.
class JWTViewSet(generics.CreateAPIView):
    serializer_class = serializers.AuthSerializer

    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def _get_token(self, user):
        key = jwk.JWK.generate(kty='RSA', size=2048)
        priv_pem = key.export_to_pem(private_key=True, password=None)
        priv_key = jwk.JWK.from_pem(priv_pem)
        pub_pem = key.export_to_pem()
        pub_key = jwk.JWK.from_pem(pub_pem)
        payload = {'user_id': user.id}
        token = jwt.generate_jwt(payload, priv_key, 'RS256', datetime.timedelta(days=1))
        JWToken.objects.create(token=token, pub_key=pub_key.export_public())
        return token

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = self.authenticate(email=email, password=password)

        if user is not None:
            print('{}:{}'.format(email, password))
            token = self._get_token(user)
            return JsonResponse(data={'status': 200, 'token': token})
        else:
            return JsonResponse(data={'status': 403})

