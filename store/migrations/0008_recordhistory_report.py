# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20170214_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordhistory',
            name='report',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='record_report', to='store.Report'),
        ),
    ]
