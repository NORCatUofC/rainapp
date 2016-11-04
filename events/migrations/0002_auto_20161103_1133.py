# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-03 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourlyprecip',
            name='end_time',
            field=models.DateTimeField(unique=True),
        ),
        migrations.AlterField(
            model_name='hourlyprecip',
            name='start_time',
            field=models.DateTimeField(unique=True),
        ),
    ]