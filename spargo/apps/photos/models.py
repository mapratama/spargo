from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class PhotoQuerySet(models.query.QuerySet):

    def is_active(self):
        return self.filter(is_active=True)


class Photo(models.Model):

    photo = ImageField(upload_to=FilenameGenerator(prefix='product-photo'),
                       default='', blank=True)
    is_active = models.BooleanField('active', default=True)
    objects = models.Manager.from_queryset(PhotoQuerySet)()

    def __unicode__(self):
        return str(self.id)
