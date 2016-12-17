# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-12 07:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='数量')),
                ('type', models.IntegerField(choices=[(0, '操作失误'), (1, '退货')], verbose_name='退送原因')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='日期')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='说明信息')),
            ],
            options={
                'verbose_name': '退送库存记录',
                'ordering': ['goods', 'amount'],
                'verbose_name_plural': '退送库存记录',
            },
        ),
        migrations.CreateModel(
            name='TransferGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_num', models.IntegerField(verbose_name='change numbers')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='datetime')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['add_date'], 'verbose_name': '类别', 'verbose_name_plural': '类别'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '客户', 'verbose_name_plural': '客户'},
        ),
        migrations.AlterModelOptions(
            name='goods',
            options={'ordering': ['goods_name', 'update_date'], 'verbose_name': '商品', 'verbose_name_plural': '商品'},
        ),
        migrations.AlterModelOptions(
            name='goodsaddrecord',
            options={'ordering': ['goods', 'number'], 'verbose_name': '增加库存记录', 'verbose_name_plural': '增加库存记录'},
        ),
        migrations.AlterModelOptions(
            name='goodsshop',
            options={'ordering': ['goods', 'remain'], 'verbose_name': '库存', 'verbose_name_plural': '库存'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ['shop_name'], 'verbose_name': '供货商', 'verbose_name_plural': '供货商'},
        ),
        migrations.RemoveField(
            model_name='goodsaddrecord',
            name='price',
        ),
        migrations.AlterField(
            model_name='category',
            name='add_date',
            field=models.DateField(auto_now_add=True, verbose_name='添加日期'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, verbose_name='类别名称'),
        ),
        migrations.AlterField(
            model_name='category',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='描述信息'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='add_date',
            field=models.DateField(auto_now_add=True, verbose_name='添加日期'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='联系地址'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='客户联系电话'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user_name',
            field=models.CharField(max_length=15, verbose_name='客户姓名'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='add_people',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='添加人'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='average_price',
            field=models.FloatField(verbose_name='进价'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='category',
            field=models.ManyToManyField(to='store.Category', verbose_name='所属类别'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='goods_name',
            field=models.CharField(max_length=15, verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='下架'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='last_price',
            field=models.FloatField(verbose_name='售价'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='recent_sell',
            field=models.DateField(blank=True, null=True, verbose_name='最近售出日期'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='update_date',
            field=models.DateField(auto_now_add=True, verbose_name='更新日期'),
        ),
        migrations.AlterField(
            model_name='goodsaddrecord',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='goodsaddrecord',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Goods', verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='goodsaddrecord',
            name='number',
            field=models.IntegerField(verbose_name='数目'),
        ),
        migrations.AlterField(
            model_name='goodsaddrecord',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='说明信息'),
        ),
        migrations.AlterField(
            model_name='goodsaddrecord',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Shop', verbose_name='供应商'),
        ),
        migrations.AlterField(
            model_name='goodsaddrecord',
            name='updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作员'),
        ),
        migrations.AlterField(
            model_name='goodsshop',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Goods', verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='goodsshop',
            name='last_updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='更新量'),
        ),
        migrations.AlterField(
            model_name='goodsshop',
            name='remain',
            field=models.IntegerField(default=0, verbose_name='库存量'),
        ),
        migrations.AlterField(
            model_name='goodsshop',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Shop', verbose_name='供应商名称'),
        ),
        migrations.AlterField(
            model_name='goodsshop',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日期'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_address',
            field=models.CharField(max_length=100, verbose_name='供货商地址'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_name',
            field=models.CharField(max_length=20, verbose_name='供货商名称'),
        ),
        migrations.AddField(
            model_name='transfergoods',
            name='from_shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_shop', to='store.Shop', verbose_name='from shop name'),
        ),
        migrations.AddField(
            model_name='transfergoods',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Goods', verbose_name='good name'),
        ),
        migrations.AddField(
            model_name='transfergoods',
            name='to_shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_name', to='store.Shop', verbose_name='to shop name'),
        ),
        migrations.AddField(
            model_name='transfergoods',
            name='updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='operator'),
        ),
        migrations.AddField(
            model_name='returnrecord',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Goods', verbose_name='商品名称'),
        ),
        migrations.AddField(
            model_name='returnrecord',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Shop', verbose_name='供货商名称'),
        ),
        migrations.AddField(
            model_name='returnrecord',
            name='updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作员'),
        ),
    ]