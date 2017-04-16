from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class Type(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photo = ImageField(upload_to=FilenameGenerator(prefix='type-photo'),
                       default='', blank=True)
    banner = ImageField(upload_to=FilenameGenerator(prefix='type-banner'),
                        default='', blank=True)
    is_active = models.BooleanField('active', default=True)

    def __unicode__(self):
        return self.name
