# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-16 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import spargo.apps.users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, null=True, unique=True, verbose_name=b'email address')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(1, b'Male'), (2, b'Female')], null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, db_index=True, max_length=30, null=True, unique=True, verbose_name=b'Mobile Number')),
                ('gcm_key', models.CharField(blank=True, default=b'', max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', spargo.apps.users.models.CustomUserManager()),
            ],
        ),
    ]