# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-18 21:47
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tree', '0007_forgotpass'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showAll', models.BooleanField(default=True)),
                ('hulu', models.BooleanField(default=False)),
                ('amazon', models.BooleanField(default=False)),
                ('amazonPrime', models.BooleanField(default=False)),
                ('googlePlay', models.BooleanField(default=False)),
                ('itunes', models.BooleanField(default=False)),
                ('netflix', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFavorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='review',
            name='text',
        ),
        migrations.AddField(
            model_name='movie',
            name='amazon',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='amazonPrime',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='googlePlay',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='hulu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='itunes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='netflix',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 18, 21, 45, 34, 838574, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='questions',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userfavorites',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tree.Movie'),
        ),
        migrations.AddField(
            model_name='userfavorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
