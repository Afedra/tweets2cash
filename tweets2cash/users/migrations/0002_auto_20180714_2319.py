# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-14 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='color',
        ),
        migrations.RemoveField(
            model_name='user',
            name='colorize_tags',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lang',
        ),
        migrations.RemoveField(
            model_name='user',
            name='theme',
        ),
        migrations.RemoveField(
            model_name='user',
            name='timezone',
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='gender'),
        ),
    ]