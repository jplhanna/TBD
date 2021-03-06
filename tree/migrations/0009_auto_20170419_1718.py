# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-19 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0008_auto_20170418_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='year',
        ),
        migrations.AddField(
            model_name='movie',
            name='popularity',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
