from django.conf.urls import patterns, url

from .views import (Create, Dashboard, Details, Preview, SentOffering,
                    AcceptOffering, PaymentChecked, Deliver, Completed,
                    Canceled)


urlpatterns = patterns('',
    url(r'^preview$', Preview.as_view(), name='preview'),
    url(r'^create$', Create.as_view(), name='create'),
    url(r'^(?P<id>\d+)$', Details.as_view(), name='details'),
    url(r'^dashboard$', Dashboard.as_view(), name='dashboard'),
    url(r'^sent_offering$', SentOffering.as_view(), name='sent_offering'),
    url(r'^accept_offering$', AcceptOffering.as_view(), name='accept_offering'),
    url(r'^payment_checked$', PaymentChecked.as_view(), name='payment_checked'),
    url(r'^deliver$', Deliver.as_view(), name='deliver'),
    url(r'^completed$', Completed.as_view(), name='completed'),
    url(r'^canceled$', Canceled.as_view(), name='canceled'),
)
