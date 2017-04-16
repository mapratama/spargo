from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class Photo(models.Model):

    photo = ImageField(upload_to=FilenameGenerator(prefix='product-photo'),
                       default='', blank=True)
    is_active = models.BooleanField('active', default=True)

    def __unicode__(self):
        return self.id
