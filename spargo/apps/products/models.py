from django.db import models

from django.core.validators import MinValueValidator

from model_utils import Choices


class ProductQuerySet(models.query.QuerySet):

    def is_active(self):
        return self.filter(is_active=True)


class Product(models.Model):

    type_product = models.ForeignKey('types.Type')
    model = models.ManyToManyField('models.Model')
    name = models.CharField(max_length=50)
    colour = models.CharField(max_length=50, blank=True, null=True)
    weight = models.FloatField(validators=[MinValueValidator(0)])
    dimension = models.CharField('Ukuran', max_length=50, blank=True, null=True)
    material = models.CharField('Bahan', max_length=50, blank=True, null=True)
    CONDITION = Choices(
        (1, 'new', 'New'),
        (2, 'second', 'Second'),
    )

    condition = models.PositiveSmallIntegerField(choices=CONDITION, default=CONDITION.new)
    description = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField('photos.Photo', related_name='products')
    price = models.FloatField(validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField('active', default=True)
    objects = models.Manager.from_queryset(ProductQuerySet)()

    def __unicode__(self):
        return self.name
