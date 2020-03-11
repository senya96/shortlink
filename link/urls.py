from django.conf.urls import url
from link.views import CreateLinkView, DeleteLinkView

urlpatterns = [
    url(r'^new_link/', CreateLinkView.as_view()),
    url(r'^delete_link/(?P<identifier>[0-9a-zA-Z\-_]+)', DeleteLinkView.as_view()),
]
