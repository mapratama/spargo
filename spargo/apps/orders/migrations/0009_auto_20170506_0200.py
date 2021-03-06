# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-05 19:00
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20170503_2302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='region',
            new_name='extra_data',
        ),
        migrations.AddField(
            model_name='order',
            name='weight',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
