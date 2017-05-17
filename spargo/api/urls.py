from django.conf.urls import include, patterns, url


urlpatterns = patterns('spargo.api.views',
    url(r'^auth/', include('spargo.api.auth.urls', namespace='auth')),
    url(r'^orders/', include('spargo.api.orders.urls', namespace='orders')),
    url(r'^payments/', include('spargo.api.payments.urls', namespace='payments')),
)
