from django.conf.urls import patterns, url

from proxy import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^(?P<bucket_name>\S+?)(?P<key>/\S*)', views.get, name='get')
)
