from django.conf.urls import url
from .views import AnalyticView, SuperUserAnalyticView

urlpatterns = [
    url(r'^my', AnalyticView.as_view()),
    url(r'^all', SuperUserAnalyticView.as_view())
]
