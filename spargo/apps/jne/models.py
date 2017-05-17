from django.db import models
from django.core.validators import MinValueValidator


class JNE(models.Model):

    code = models.CharField(max_length=20)
    region = models.CharField(max_length=50)
    regular_cost = models.FloatField(validators=[MinValueValidator(0)])
    regular_estimated = models.PositiveSmallIntegerField(blank=True, null=True)
    oke_cost = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    oke_estimated = models.PositiveSmallIntegerField(blank=True, null=True)
    yes_cost = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    yes_estimated = models.PositiveSmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.region
