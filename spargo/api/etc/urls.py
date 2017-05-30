from django.conf.urls import patterns, url

from .views import SyncData


urlpatterns = patterns('',
    url(r'^sync_data$', SyncData.as_view(), name='sync_data')
)
