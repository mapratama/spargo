from django.db import models

from django.core.validators import MinValueValidator

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class Order(models.Model):

    user = models.ForeignKey('users.User', related_name='orders')
    number = models.CharField(max_length=10, db_index=True)
    STATUS = Choices(
        (1, 'new', 'New'),
        (2, 'deliver', 'Deliver'),
        (3, 'completed', 'Completed'),
        (4, 'canceled', 'Canceled'),
        (5, 'rejected', 'Rejected'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.new)
    created = AutoCreatedField()
    price = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    notes = models.TextField(default='', blank=True)

    def __unicode__(self):
        return 'Booking #%s' % (self.code)


class Item(models.Model):
    booking = models.ForeignKey(Order, related_name='items')
    quantity = models.PositiveSmallIntegerField()
    price = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    product = models.ForeignKey('products.Product', related_name='items')
