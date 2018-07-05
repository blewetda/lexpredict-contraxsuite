# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-06 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0011_taskconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskconfig',
            name='id',
        ),
        migrations.AlterField(
            model_name='taskconfig',
            name='name',
            field=models.CharField(db_index=True, max_length=100, primary_key=True, serialize=False),
        ),
    ]
