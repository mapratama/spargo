from django.conf.urls import url

from .views import Add

urlpatterns = [
    url(r'^add$', Add.as_view(), name='add'),
]
