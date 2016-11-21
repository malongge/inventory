#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Created by thomas on 2015/8/25
#


from django.core.management.base import BaseCommand
from store.models import Shop, Goods, Category
from exceltojson import excel2json, utils
from django.contrib.auth.models import User
from datetime import datetime

class Command(BaseCommand):
    help = '将给定的表，导入到数据库当中'

    def _format_time(self, str_time):
        return datetime.strptime(str_time, '%Y/%m/%d')

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--path',
            dest='excel_path',
            help='需要导入到数据库的 excel 文件路径'
        )

    def handle(self, *args, **options):
        path = options['excel_path']
        sheet = utils.get_sheets(path)[0]
        alais = {'商品名称': 'good_name', '库存量': 'remain', '单位': 'unit',
                 '售价': 'sell_price', '所属类别': 'category', '有效期': 'time',
                 '供货商': 'shop', '进价': 'average_price'}
        sheet_process = excel2json._SheetProcess(sheet, alias=alais, merge_cell=False)
        shops = set()
        cates = set()
        add_people = User.objects.all()[0]
        goods = set()

        try:
            default_cate = Category.objects.get(name='未分类商品')
        except Exception as e:
            default_cate = Category.objects.create(name='未分类商品')

        for data in sheet_process():
            print('index--------' + str(data[0]))
            details = data[1]
            try:
                if not details['shop'].strip():
                    s = None
                else:
                    s = Shop.objects.get(shop_name=details['shop'])
                    if details['shop'] in shops:
                        pass
                    else:
                        print('已存在供货商: '+details['shop'])
            except Exception as e:
                s = Shop.objects.create(shop_name=details['shop'])
                shops.add(details['shop'])

            try:
                if not details['category'].strip():
                    cate = default_cate
                else:
                    cate = Category.objects.get(name=details['category'])
                    if details['category'] not in cates:
                        print('已存在类别: ' + details['category'])
            except Exception as e:
                cate = Category.objects.create(name=details['category'])
                cates.add(details['category'])

            try:
                Goods.objects.get(goods_name=details['good_name'])
                if details['good_name'] not in goods:
                    print('已存在商品: ' + details['good_name'])
            except Exception as e:
                try:
                    ap = 0 if not details['average_price'].strip() else float(details['average_price'])
                    lp = 0 if not details['sell_price'].strip() else float(details['sell_price'])
                    rm = 0 if not details['remain'].strip() else int(float(details['remain']))
                    time = self._format_time('2017/10/30') if not details['time'].strip() else self._format_time(details['time'])
                    print(details['average_price'])
                    print(details['sell_price'])
                    print(details['remain'])
                    g = Goods.objects.create(
                        goods_name=details['good_name'],
                        average_price=ap,
                        last_price=lp,
                        unit_name=details['unit'],
                        add_people=add_people,
                        remain=rm,
                        last_time=time,
                        shop=s
                    )

                    g.category.add(cate)
                    goods.add(details['good_name'])
                except Exception as e:
                    print(str(e))
                    print(data[1])
                    break
