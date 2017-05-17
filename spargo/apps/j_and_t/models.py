from django.db import models
from django.core.validators import MinValueValidator


class JAndT(models.Model):

    code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    cost = models.FloatField(validators=[MinValueValidator(0)])

    def __unicode__(self):
        return self.city
