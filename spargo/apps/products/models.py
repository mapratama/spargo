from django.db import models

from django.core.validators import MinValueValidator


class Product(models.Model):

    type = models.OneToOneField('categories.Category')
    model = models.OneToOneField('models.Model')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField('photos.Photo', related_name='types')
    price = models.FloatField(validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField('active', default=True)

    def __unicode__(self):
        return self.name
