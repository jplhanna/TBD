# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-27 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0002_auto_20170327_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]