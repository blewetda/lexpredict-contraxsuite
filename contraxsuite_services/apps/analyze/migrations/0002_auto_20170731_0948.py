# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 09:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analyze', '0001_initial'),
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textunitsimilarity',
            name='text_unit_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_text_unit_a_set', to='document.TextUnit'),
        ),
        migrations.AddField(
            model_name='textunitsimilarity',
            name='text_unit_b',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_text_unit_b_set', to='document.TextUnit'),
        ),
        migrations.AddField(
            model_name='textunitcluster',
            name='text_units',
            field=models.ManyToManyField(blank=True, to='document.TextUnit'),
        ),
        migrations.AddField(
            model_name='textunitclassifiersuggestion',
            name='classifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyze.TextUnitClassifier'),
        ),
        migrations.AddField(
            model_name='textunitclassifiersuggestion',
            name='text_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.TextUnit'),
        ),
        migrations.AlterUniqueTogether(
            name='textunitclassifier',
            unique_together=set([('name', 'version')]),
        ),
        migrations.AddField(
            model_name='textunitclassification',
            name='text_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.TextUnit'),
        ),
    ]
