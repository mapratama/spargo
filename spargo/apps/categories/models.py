from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class Category(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photo = ImageField(upload_to=FilenameGenerator(prefix='category-photo'),
                       default='', blank=True)
    banner = ImageField(upload_to=FilenameGenerator(prefix='category-banner'),
                        default='', blank=True)
    is_active = models.BooleanField('active', default=True)

    def __unicode__(self):
        return self.name
