# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 03:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('creditcards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
    ]
