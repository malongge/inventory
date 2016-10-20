#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Created by thomas on 2015/8/25
#


from django.core.management.base import BaseCommand
from django.core.cache import cache
from store.models import Goods, Category

class Command(BaseCommand):
    help = '所有商品均添加到第一个类别当中'

    def handle(self, *args, **options):
        goods = Goods.objects.all()
        cate = Category.objects.all()[0]
        for g in goods:
            if not g.category:
                g.category = cate
                g.save()

