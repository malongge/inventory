# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-11 08:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(verbose_name='category description')),
                ('name', models.CharField(max_length=20, verbose_name='category name')),
                ('add_date', models.DateField(auto_now_add=True, verbose_name='add date')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=15, verbose_name='customer name')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='customer address')),
                ('phone_number', models.CharField(max_length=20, verbose_name='customer phone number')),
                ('add_date', models.DateField(auto_now_add=True, verbose_name='add date')),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=15, verbose_name='good name')),
                ('average_price', models.FloatField(verbose_name='average price')),
                ('last_price', models.FloatField(verbose_name='current price')),
                ('update_date', models.DateField(auto_now_add=True, verbose_name='update date')),
                ('recent_sell', models.DateField(blank=True, null=True, verbose_name='recent sell')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is delete')),
                ('add_people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='add people')),
                ('category', models.ManyToManyField(to='store.Category', verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsAddRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='number')),
                ('price', models.FloatField(verbose_name='price')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='description')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='datetime')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Goods', verbose_name='good name')),
                ('updater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='operator')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsSellRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_num', models.IntegerField(verbose_name='sell numbers')),
                ('average_price', models.FloatField(verbose_name='average price')),
                ('sell_price', models.FloatField(verbose_name='sell price')),
                ('is_arrears', models.BooleanField(verbose_name='arrears or not')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_delete', models.BooleanField(default=False, verbose_name='delete or not')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='datetime')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remain', models.IntegerField(verbose_name='remain')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='update date')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Goods', verbose_name='good name')),
                ('last_updater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='updater')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='志平电子配件销售清单', max_length=100, verbose_name='name')),
                ('ad', models.TextField(default='专业批发: 电视， 冰箱...', verbose_name='ad title')),
                ('is_arrears', models.BooleanField(verbose_name='arrears or not')),
                ('phone', models.CharField(default='7566409 13755519477', max_length=50, verbose_name='phone number')),
                ('address', models.CharField(default='芦溪县凌云南路太阳城B栋良友旁', max_length=50, verbose_name='address')),
                ('remark', models.TextField(blank=True, default='银行卡号: 6222.0215 0400 3618 261\n中国银行: 6216 6165 0600 0292 464', null=True, verbose_name='description')),
                ('all_price', models.FloatField(default=0, verbose_name='total price')),
                ('all_profit', models.FloatField(default=0, verbose_name='total profit')),
                ('is_delete', models.BooleanField(default=False, verbose_name='delete or not')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='datetime')),
                ('arrears_price', models.FloatField(default=0, verbose_name='arrears price')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('customer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.Customer')),
                ('shop_name', models.CharField(max_length=20, verbose_name='shop name')),
                ('shop_address', models.CharField(max_length=100, verbose_name='shop address')),
            ],
            bases=('store.customer',),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Customer', verbose_name='customer name'),
        ),
        migrations.AddField(
            model_name='order',
            name='updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='operator'),
        ),
        migrations.AddField(
            model_name='goodssellrecord',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='store.Customer', verbose_name='customer name'),
        ),
        migrations.AddField(
            model_name='goodssellrecord',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='store.Goods', verbose_name='good name'),
        ),
        migrations.AddField(
            model_name='goodssellrecord',
            name='updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL, verbose_name='operator'),
        ),
        migrations.AddField(
            model_name='goodsshop',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Shop', verbose_name='shop name'),
        ),
        migrations.AddField(
            model_name='goodssellrecord',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='store.Shop', verbose_name='shop name'),
        ),
        migrations.AddField(
            model_name='goodsaddrecord',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Shop', verbose_name='shop name'),
        ),
    ]
