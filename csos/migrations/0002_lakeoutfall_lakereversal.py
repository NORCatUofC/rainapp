# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-04 16:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LakeOutfall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LakeReversal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_date', models.DateField()),
                ('close_date', models.DateField()),
                ('millions_of_gallons', models.FloatField()),
                ('lake_outfall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csos.LakeOutfall')),
            ],
        ),
    ]
