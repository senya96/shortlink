from django.conf.urls import url
from jwt_auth.views import JWTViewSet

urlpatterns = [
    url(r'^auth/', JWTViewSet.as_view())
]
