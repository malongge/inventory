# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-17 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20161217_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnrecord',
            name='reset_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='还原价格'),
        ),
    ]
