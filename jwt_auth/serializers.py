from rest_framework import serializers


class JWTSerializer(serializers.Serializer):
    token = serializers.CharField()


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
