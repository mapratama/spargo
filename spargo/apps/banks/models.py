from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class BankQuerySet(models.query.QuerySet):

    def is_active(self):
        return self.filter(is_active=True)


class Bank(models.Model):

    name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)
    photo = ImageField(upload_to=FilenameGenerator(prefix='model-photo'),
                       default='', blank=True)
    is_active = models.BooleanField('active', default=True)
    objects = models.Manager.from_queryset(BankQuerySet)()

    def __unicode__(self):
        return self.name
