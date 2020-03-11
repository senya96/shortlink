# Serializers define the API representation.
from django.contrib.auth.models import User
from django.db.models import Count, Prefetch, Sum
from django.http import JsonResponse
from rest_framework import views
import datetime

from jwt_auth.decorators import auth_required
from . import serializers
from link.serializers import serializers as link_serializers
from link.models import LinkModel


# Create your views here.

class AnalyticView(views.APIView):

    @auth_required(superuser_required=False)
    def get(self, request):
        date_from = request.GET.get('from', None)
        date_to = request.GET.get('to', None)
        sort = request.GET.get('sort', None)
        links = LinkModel.objects.filter(owner=request.user).prefetch_related('linkvisitinfo_set')
        if date_from:
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            links = links.filter(linkvisitinfo__date__gte=date_from)
        if date_to:
            date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            links = links.filter(linkvisitinfo__date__lte=date_to)
        links = links.annotate(visits=Count('linkvisitinfo'))
        if sort == 'inc':
            links = links.order_by('visits')
        elif sort == 'dec':
            links = links.order_by('-visits')

        data = link_serializers.LinkVisitsSerializer(links, context={'request': request}, many=True)
        return JsonResponse(data=data.data, safe=False)


class SuperUserAnalyticView(views.APIView):

    @auth_required(superuser_required=True)
    def get(self, request):
        def get_link_query(d_to, d_from):
            links = LinkModel.objects.all().prefetch_related('linkvisitinfo_set')
            if d_from:
                d_from = datetime.datetime.strptime(d_from, '%Y-%m-%d')
                links = links.filter(linkvisitinfo__date__gte=d_from)
            if d_to:
                d_to = datetime.datetime.strptime(d_to, '%Y-%m-%d')
                links = links.filter(linkvisitinfo__date__lte=d_to)
            links = links.annotate(visits=Count('linkvisitinfo', distinct=True)).order_by('-visits')
            links_id = list()
            for link in links[:5]:
                links_id.append(link.id)
            links = links.filter(id__in=links_id)
            return links
        date_from = request.GET.get('from', None)
        date_to = request.GET.get('to', None)
        users = User.objects.all().prefetch_related(
            Prefetch(
                'linkmodel_set',
                queryset=get_link_query(date_to, date_from)
            )
        )
        # users = users.distinct()
        data = serializers.UserAnalyticSerializer(users, context={'request': request}, many=True)
        return JsonResponse(data=data.data, safe=False)

