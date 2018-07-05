# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-30 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_auto_20180510_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadsession',
            name='notified_upload_completed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='uploadsession',
            name='notified_upload_started',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
