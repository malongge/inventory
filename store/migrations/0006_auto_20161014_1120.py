# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 03:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_goodssellrecord_arrears_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='志平电子配件销售清单', max_length=100, verbose_name='标题')),
                ('alias', models.CharField(default='默认模板', max_length=20, verbose_name='模板名字')),
                ('ad', models.TextField(verbose_name='广告语')),
                ('phone', models.CharField(default='7566409 13755519477', max_length=50, verbose_name='电话号码')),
                ('address', models.CharField(default='芦溪县凌云南路太阳城B栋良友旁', max_length=50, verbose_name='地址')),
                ('remark', models.TextField(blank=True, default='银行卡号: 6222.0215 0400 3618 261\n中国银行: 6216 6165 0600 0292 464', null=True, verbose_name='附加信息')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='日期')),
            ],
            options={
                'verbose_name_plural': '设置清单',
                'ordering': ['-date'],
                'verbose_name': '设置清单',
            },
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date'], 'verbose_name': '订单记录', 'verbose_name_plural': '订单记录'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='ad',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='arrears_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_arrears',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='remark',
        ),
        migrations.AlterField(
            model_name='goodssellrecord',
            name='average_price',
            field=models.FloatField(blank=True, null=True, verbose_name='调整进价'),
        ),
        migrations.AlterField(
            model_name='goodssellrecord',
            name='sell_price',
            field=models.FloatField(blank=True, null=True, verbose_name='调整售价'),
        ),
        migrations.AlterField(
            model_name='order',
            name='all_price',
            field=models.FloatField(default=0, verbose_name='总价'),
        ),
        migrations.AlterField(
            model_name='order',
            name='all_profit',
            field=models.FloatField(default=0, verbose_name='总利润'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Customer', verbose_name='客户名称'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否取消订单'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作人员'),
        ),
        migrations.AddField(
            model_name='order',
            name='report',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.Report', verbose_name='清单模板'),
            preserve_default=False,
        ),
    ]
