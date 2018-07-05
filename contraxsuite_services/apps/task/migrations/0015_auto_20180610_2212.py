# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-10 22:12
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0014_auto_20180606_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltask',
            name='celery_task_result',
        ),
        migrations.RemoveField(
            model_name='historicaltask',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltask',
            name='user',
        ),
        migrations.RemoveField(
            model_name='task',
            name='celery_task_result',
        ),
        migrations.RemoveField(
            model_name='task',
            name='subtasks_processed',
        ),
        migrations.RemoveField(
            model_name='task',
            name='subtasks_total',
        ),
        migrations.AddField(
            model_name='task',
            name='hidden',
            field=models.BooleanField(db_index=True, default=False, editable=False),
        ),
        migrations.AddField(
            model_name='task',
            name='result',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='traceback',
            field=models.TextField(blank=True, null=True, verbose_name='traceback'),
        ),
        migrations.AlterField(
            model_name='task',
            name='_status',
            field=models.CharField(blank=True, choices=[('FAILURE', 'FAILURE'), ('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('RETRY', 'RETRY'), ('REVOKED', 'REVOKED'), ('STARTED', 'STARTED'), ('SUCCESS', 'SUCCESS')], db_index=True, default='PENDING', max_length=50, null=True, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='task',
            name='celery_task_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='task id'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='HistoricalTask',
        ),
    ]
