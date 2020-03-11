from rest_framework import serializers

from link.serializers import LinkVisitsSerializer


class UserAnalyticSerializer(serializers.Serializer):
    email = serializers.CharField()
    linkmodel_set = LinkVisitsSerializer(many=True)

