# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-26 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20170426_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='with_installation',
            field=models.BooleanField(default=True),
        ),
    ]
