# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-12 08:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20161012_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transfergoods',
            options={'ordering': ['goods', 'change_num'], 'verbose_name': '直接交易记录', 'verbose_name_plural': '直接交易记录'},
        ),
        migrations.AddField(
            model_name='transfergoods',
            name='from_price',
            field=models.FloatField(default=0, verbose_name='进价'),
        ),
        migrations.AddField(
            model_name='transfergoods',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='说明信息'),
        ),
        migrations.AddField(
            model_name='transfergoods',
            name='to_price',
            field=models.FloatField(default=0, verbose_name='售价'),
        ),
        migrations.AlterField(
            model_name='transfergoods',
            name='change_num',
            field=models.IntegerField(verbose_name='交易数量'),
        ),
        migrations.AlterField(
            model_name='transfergoods',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='transfergoods',
            name='from_shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_shop', to='store.Shop', verbose_name='供应商'),
        ),
        migrations.AlterField(
            model_name='transfergoods',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Goods', verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='transfergoods',
            name='to_shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_name', to='store.Shop', verbose_name='销售商'),
        ),
        migrations.AlterField(
            model_name='transfergoods',
            name='updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作人员'),
        ),
    ]
