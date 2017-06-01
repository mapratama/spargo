from django.db import models

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator


class CategoryQuerySet(models.query.QuerySet):

    def is_active(self):
        return self.filter(is_active=True)


class Category(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photo = ImageField(upload_to=FilenameGenerator(prefix='category-photo'),
                       default='', blank=True)
    is_active = models.BooleanField('active', default=True)
    model = models.ManyToManyField('models.Model')
    objects = models.Manager.from_queryset(CategoryQuerySet)()

    def __unicode__(self):
        return self.name
