# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-25 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='thintused',
            name='hint',
        ),
        migrations.RemoveField(
            model_name='thintused',
            name='team',
        ),
        migrations.RemoveField(
            model_name='unlockedchallenge',
            name='challenge',
        ),
        migrations.RemoveField(
            model_name='unlockedchallenge',
            name='team',
        ),
        migrations.RenameField(
            model_name='hints',
            old_name='penaly',
            new_name='penalty',
        ),
        migrations.AddField(
            model_name='challenge',
            name='unlockedBy',
            field=models.ManyToManyField(to='team.Team'),
        ),
        migrations.AddField(
            model_name='hints',
            name='usedBy',
            field=models.ManyToManyField(to='team.Team'),
        ),
        migrations.DeleteModel(
            name='tHintUsed',
        ),
        migrations.DeleteModel(
            name='unlockedChallenge',
        ),
        migrations.AddField(
            model_name='challenge',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenges.Category'),
        ),
    ]
