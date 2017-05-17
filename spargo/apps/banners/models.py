from django.db import models

from spargo.core.utils import FilenameGenerator

from thumbnails.fields import ImageField


class BannerQuerySet(models.query.QuerySet):

    def is_active(self):
        return self.filter(is_active=True)


class Banner(models.Model):

    photo = ImageField(upload_to=FilenameGenerator(prefix='banner-photo'),
                       default='', blank=True)
    is_active = models.BooleanField('aktif', default=True)
    objects = models.Manager.from_queryset(BannerQuerySet)()

    def __unicode__(self):
        return str(self.id)
