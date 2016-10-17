from django.contrib import admin
from .models import *
from django.db import transaction
from django.core.exceptions import PermissionDenied


class GoddsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('goods_name', 'average_price', 'last_price', 'remain', 'category')
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('recent_sell', 'is_delete', 'shop')
        }),
    )
    list_display = (
    'goods_name', 'average_price', 'last_price',  'remain', 'recent_sell', 'is_delete', 'add_people', 'update_date')
    list_filter = ['category']
    search_fields = ['goods_name']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'add_people', None) is None:
            obj.add_people = request.user
        obj.save()


class CustomsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user_name', 'address', 'phone_number', )
        }),
    )
    list_display = ('user_name', 'address', 'phone_number', )
    search_fields = ['user_name']


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'remark', 'super_category')
        }),
    )
    list_display = ('name', 'remark', 'super_category', 'add_date',)
    search_fields = ['name']


class ShopAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user_name', 'shop_name', 'phone_number', 'shop_address',)
        }),
    )
    list_display = ('user_name', 'shop_name', 'phone_number', 'shop_address', 'add_date',)
    search_fields = ['shop_name']


# class GoodsShopAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {
#             'fields': ('goods', 'shop', 'remain', )
#         }),
#     )
#     list_display = ('goods', 'shop', 'remain', 'add_people', 'update_date',)
#     search_fields = ['goods', 'shop']
#
#     def save_model(self, request, obj, form, change):
#         if getattr(obj, 'last_updater', None) is None:
#             obj.last_updater = request.user
#         obj.save()


class GoodsAddRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('goods', 'shop', 'number', )
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('remark', 'new_price')
        }),
    )
    list_display = ('goods', 'shop', 'number', 'remark', 'updater', 'date', 'new_price')
    search_fields = ['goods', 'shop']

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user
        records = Goods.objects.filter(goods=obj.goods)
        if records:
            record = records[0]

            if obj.new_price:
                record.average_price = (obj.new_price * obj.number + record.remain * record.average_price) / \
                                       (record.remain + obj.number)
            record.remain = record.remain + obj.number
            record.save()
        else:
            raise Exception('商品还不存在，无法增加库存')
        obj.save()


class ReturnRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('goods', 'shop', 'amount', 'type')
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('remark',)
        }),
    )
    list_display = ('goods', 'shop', 'amount', 'type', 'remark', 'updater', 'date')
    search_fields = ['goods', 'shop']

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user
        records = Goods.objects.filter(goods=obj.goods, shop=obj.shop)
        if records:
            record = records[0]
            record.remain = record.remain + obj.amount
            record.save()
        else:
            raise Exception("库存中还没有这个商品无法进行退送")
        obj.save()


class TransferGoodsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('goods', 'from_shop', 'to_shop', 'from_price', 'to_price', 'change_num')
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('remark',)
        }),
    )
    list_display = ('goods', 'from_shop', 'to_shop', 'from_price', 'to_price', 'change_num', 'remark', 'updater', 'date')
    search_fields = ['goods', 'from_shop', 'to_shop']


    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user

        obj.save()


class GoodsSellRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('goods', 'shop', 'sell_num', 'customer')
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('remark', 'is_arrears', 'arrears_price', 'average_price', 'sell_price',)
        }),
    )
    list_display = ('goods', 'shop', 'sell_num', 'average_price', 'sell_price', 'customer', 'is_arrears',
                    'arrears_price', 'remark', 'updater', 'date')
    search_fields = ['goods', 'shop']

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user
        records = Goods.objects.filter(goods=obj.goods, shop=obj.shop)
        if records:
            record = records[0]
            record.remain = record.remain - obj.sell_num
            if record.remain < 0:
                raise PermissionDenied("库存不够，需要补充库存")
            record.save()
            # goods = Goods.objects.get(goods=obj.goods)
            obj.average_price = obj.goods.average_price
            obj.sell_price = obj.goods.last_price
        else:
            raise PermissionDenied("库存中还没有这个商品， 无法销售")
        obj.save()


class OrderMixin(object):

    change_list_template = 'admin/liuzhiping/change_list.html'
    report_template = 'admin/liuzhiping/report.html'

    def get_model_info(self):
        # module_name is renamed to model_name in Django 1.8
        app_label = self.model._meta.app_label
        try:
            return (app_label, self.model._meta.model_name,)
        except AttributeError:
            return (app_label, self.model._meta.module_name,)

from django.utils.encoding import force_text
from django.contrib.admin.options import csrf_protect_m
from django.conf.urls import url
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

class OrderAdmin(OrderMixin, admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        categories = Category.objects.all()
        goods = Goods.objects.filter(category=categories[0])
        extra_context = {'categories': categories, 'goods': goods}
        return super(OrderAdmin, self).changelist_view(request, extra_context)

    def goods_list_view(self, request, cat_id):
        goods = Goods.objects.filter(category=cat_id)
        ret = []
        for g in goods:
            data = {}
            data['name'] = g.goods_name
            data['price'] = g.last_price
            data['remain'] = g.remain
            data['unit'] = g.unit_name
            data['id'] = g.id
            ret.append(data)
        return HttpResponse(json.dumps(ret), content_type="application/json")

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        my_urls = [
            url(r'^goods-list/(\d+)/$',
                self.admin_site.admin_view(self.goods_list_view),
                name='%s_%s_goods-list' % self.get_model_info()),
            url(r'^report/$',
                self.admin_site.admin_view(self.report_view),
                name='%s_%s_report' % self.get_model_info()),
        ]
        return my_urls + urls

    def report_view(self, request):
        data = []
        # for key, value in json.loads(request.POST['data_list']).items():
        #     g = Goods.objects.get(id=key)
        #     g.num = value
        #     data.append(g)
        for obj in Goods.objects.all():
            obj.num = 1
            data.append(obj)

        default_report = Report.objects.filter(tag=True).order_by('-date')[0]

        return render(request, context={'data': data, 'report': default_report}, template_name=self.report_template)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'alias', 'ad', 'phone', 'address', 'remark', 'date',
                    'tag')
    search_fields = ['title', 'alias', 'remark']

admin.site.register(Goods, GoddsAdmin)
admin.site.register(Customer, CustomsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
# admin.site.register(GoodsShop, GoodsShopAdmin)
admin.site.register(TransferGoods, TransferGoodsAdmin)
admin.site.register(GoodsAddRecord, GoodsAddRecordAdmin)
admin.site.register(ReturnRecord, ReturnRecordAdmin)
admin.site.register(GoodsSellRecord, GoodsSellRecordAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Report, ReportAdmin)
