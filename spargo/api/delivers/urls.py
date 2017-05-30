from django.conf.urls import patterns, url

from .views import ListJNE, ListJNT


urlpatterns = patterns('',
    url(r'^jne$', ListJNE.as_view(), name='jne'),
    url(r'^jnt$', ListJNT.as_view(), name='jnt'),
)
