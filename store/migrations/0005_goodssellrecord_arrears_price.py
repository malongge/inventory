# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-12 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20161012_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodssellrecord',
            name='arrears_price',
            field=models.FloatField(blank=True, null=True, verbose_name='欠款额'),
        ),
    ]