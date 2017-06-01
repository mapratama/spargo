from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class TypeQuerySet(models.query.QuerySet):

    def is_active(self):
        return self.filter(is_active=True)


class Type(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photo = ImageField(upload_to=FilenameGenerator(prefix='type-photo'),
                       default='', blank=True)
    is_active = models.BooleanField('active', default=True)
    objects = models.Manager.from_queryset(TypeQuerySet)()

    def __unicode__(self):
        return self.name
