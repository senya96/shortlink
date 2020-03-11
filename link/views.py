# Serializers define the API representation.
from django.db.models import F, Count
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from rest_framework import generics, views
import datetime

from jwt_auth.decorators import auth_required
from . import serializers
from .models import LinkModel, LinkVisitInfo, DELETED_STATUS
from utils import get_base64_string


# ViewSets define the view behavior.
class CreateLinkView(generics.CreateAPIView):
    serializer_class = serializers.CreateLinkSerializer

    @auth_required(superuser_required=False)
    def post(self, request, *args, **kwargs):
        original_link = request.POST['link']
        identifier = get_base64_string()
        while LinkModel.objects.filter(identifier=identifier):
            identifier = get_base64_string()
        link = LinkModel.objects.create(identifier=identifier, original_link=original_link, owner=request.user)
        data = serializers.LinkSerializer(link, context={'request': request})
        return JsonResponse(data=data.data)


# ViewSets define the view behavior.
class RedirectLinkView(views.APIView):

    def get(self, request, identifier):
        link = LinkModel.objects.get(identifier=identifier)
        if link.status == DELETED_STATUS:
            raise Http404
        LinkVisitInfo.objects.create(link=link)
        return redirect(link.original_link)


class DeleteLinkView(views.APIView):

    @auth_required(superuser_required=False)
    def get(self, request, identifier):
        link = LinkModel.objects.get(identifier=identifier, owner=request.user)
        if link:
            link.status = DELETED_STATUS
            link.save()
            return JsonResponse(data={'msg': 'Link deleted.'})
        else:
            return JsonResponse(data={'msg': 'ERROR: Link does not exist or you are not owner.'})
