import random

from thumbnails.fields import ImageField

from spargo.core.utils import FilenameGenerator

from django.db import models
from django.core.validators import MinValueValidator

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class OrderQuerySet(models.query.QuerySet):

    def is_active(self):
        return self.exclude(
            status__in=[Order.STATUS.completed, Order.STATUS.canceled]
        )


class Order(models.Model):

    user = models.ForeignKey('users.User', related_name='orders')
    invoice_number = models.CharField(max_length=10, db_index=True)
    code = models.CharField(max_length=3, db_index=True)

    STATUS = Choices(
        (1, 'new', 'New'),
        (2, 'pending', 'Pending'),
        (3, 'installation_bid', 'Installation Bid'),
        (4, 'created', 'Created'),
        (5, 'paid', 'Paid'),
        (6, 'payment_approved', 'Payment Approved'),
        (7, 'deliver', 'Deliver'),
        (8, 'completed', 'Completed'),
        (9, 'canceled', 'Canceled'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.new)

    DELIVER_TYPE = Choices(
        (1, 'jne', 'JNE'),
        (2, 'jnt_express', 'JNT Express'),
        (3, 'spargo', 'Spargo Kurir'),
    )

    deliver_type = models.PositiveSmallIntegerField(choices=DELIVER_TYPE)
    price = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    with_installation = models.BooleanField(default=True)
    installation_fee = models.FloatField(validators=[MinValueValidator(0)], default=0)
    delivery_fee = models.FloatField(validators=[MinValueValidator(0)], default=0)
    delivery_id = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField()
    extra_data = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    notes = models.TextField(default='', blank=True)
    created = AutoCreatedField()
    objects = models.Manager.from_queryset(OrderQuerySet)()

    def __unicode__(self):
        return 'Order #%s' % (self.invoice_number)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = ''.join(random.choice('12346789ACFHJKLTUXZ')
                                          for i in range(10))
        if not self.code:
            code = ''.join(random.choice('123467890') for i in range(3))
            self.code = code
            self.price = self.price + float(code)
        booking = super(Order, self).save(*args, **kwargs)
        return booking


class Item(models.Model):
    order = models.ForeignKey('orders.Order', related_name='items')
    quantity = models.PositiveSmallIntegerField()
    price = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    product = models.ForeignKey('products.Product', related_name='items')
    notes = models.TextField(default='', blank=True)


class Payment(models.Model):
    order = models.ForeignKey('orders.Order', related_name='payments')
    bank = models.ForeignKey('banks.Bank')
    sender = models.CharField(max_length=50)
    created = AutoCreatedField()
    STATUS = Choices(
        (1, 'new', 'New'),
        (2, 'accepted', 'Accepted'),
        (3, 'rejected', 'Rejected')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.new)
    photo = ImageField(upload_to=FilenameGenerator(prefix='payment_confirmations'),
                       resize_source_to='size_400', default='', blank=True)
    correction_by = models.ForeignKey('users.User', related_name='payment_confirmations', blank=True, null=True)
    notes = models.TextField(default='', blank=True)

    def __unicode__(self):
        return 'Order-%s' % self.order.code
