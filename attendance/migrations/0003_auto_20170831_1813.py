# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 12:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20170831_1811'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preclaim',
            old_name='roll_numbers',
            new_name='add_roll_numbers',
        ),
    ]
