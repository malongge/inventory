#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Created by thomas on 2015/8/25
#


from django.core.management.base import BaseCommand
from store.models import Shop, Shops

class Command(BaseCommand):
    help = '所有商品均添加到第一个类别当中'

    def handle(self, *args, **options):
        shops = Shop.objects.all()

        for s in shops:
            d = s.__dict__
            d.pop('customer_ptr_id')
            d.pop('_state')
            print(d)
            Shops.objects.create(**d)



