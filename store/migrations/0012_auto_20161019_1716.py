# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-19 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20161019_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='last_time',
            field=models.DateField(blank=True, null=True, verbose_name='有效期'),
        ),
        migrations.AlterField(
            model_name='goodssellrecord',
            name='average_price',
            field=models.FloatField(blank=True, null=True, verbose_name='进价'),
        ),
        migrations.AlterField(
            model_name='goodssellrecord',
            name='is_arrears',
            field=models.BooleanField(default=False, verbose_name='是否欠款'),
        ),
        migrations.AlterField(
            model_name='goodssellrecord',
            name='sell_price',
            field=models.FloatField(blank=True, null=True, verbose_name='售价'),
        ),
    ]
