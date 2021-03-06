# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0006_auto_20161225_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remotePath', models.CharField(max_length=255)),
                ('localPath', models.CharField(max_length=255)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.Challenge')),
            ],
        ),
    ]
