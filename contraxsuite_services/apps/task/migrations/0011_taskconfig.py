# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-06 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_auto_20180510_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('max_retries', models.PositiveIntegerField(blank=True, null=True)),
                ('soft_time_limit', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
    ]
