from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class Model(models.Model):

    category = models.OneToOneField('categories.Category')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photo = ImageField(upload_to=FilenameGenerator(prefix='model-photo'),
                       default='', blank=True)
    is_active = models.BooleanField('active', default=True)

    def __unicode__(self):
        return self.name
