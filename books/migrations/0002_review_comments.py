# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]