from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<level>[a-z]+)/(?P<year>[0-9]+)/$', views.filter, name='filter'),
]
