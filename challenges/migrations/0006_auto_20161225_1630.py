# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-25 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_auto_20161225_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengeseen',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='solvedchallenge',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='wrongsubmisson',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
