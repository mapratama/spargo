# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-01 08:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='banner',
        ),
    ]