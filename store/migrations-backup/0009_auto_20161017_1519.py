# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-17 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20161016_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodsshop',
            name='goods_ptr',
        ),
        migrations.AddField(
            model_name='goods',
            name='unit_name',
            field=models.CharField(default='件', max_length=10, verbose_name='单位'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goodsaddrecord',
            name='new_price',
            field=models.FloatField(blank=True, null=True, verbose_name='新进价'),
        ),
        migrations.DeleteModel(
            name='GoodsShop',
        ),
    ]