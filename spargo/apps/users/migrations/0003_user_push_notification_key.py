# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-22 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170416_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='push_notification_key',
            field=models.CharField(blank=True, default=b'', max_length=254),
        ),
    ]
