# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_auto_20170831_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='name',
        ),
        migrations.AddField(
            model_name='batch',
            name='batch',
            field=models.CharField(choices=[('a', 'A'), ('b', 'B')], default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='batch',
            name='semester',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
