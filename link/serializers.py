from rest_framework import serializers


class CreateLinkSerializer(serializers.Serializer):
    original_link = serializers.CharField()


class LinkSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    original_link = serializers.CharField()
    status = serializers.IntegerField()
    shortlink = serializers.SerializerMethodField()

    def get_shortlink(self, obj):
        request = self.context.get('request')
        url = f'http://{request.META["HTTP_HOST"]}/{obj.identifier}'
        return url


class LinkVisitsSerializer(LinkSerializer):
    visits = serializers.IntegerField()
