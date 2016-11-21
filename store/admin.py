from django.contrib import admin
from .models import *
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

Max_Row = 13
class GoddsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('goods_name', 'average_price', 'last_price', 'unit_name', 'last_time', 'remain', 'category')
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('recent_sell', 'is_delete', 'shop')
        }),
    )
    list_display = (
    'goods_name', 'unit_name', 'average_price', 'last_price',  'remain', 'sell_amount', 'in_amount', 'own_amount',
    'last_time', 'add_people', 'update_date')
    list_filter = ['category']
    search_fields = ['goods_name']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'add_people', None) is None:
            obj.add_people = request.user

        # if not getattr(obj, 'category', None):
        #     raise ValidationError('未填写商品种类')
        obj.save()

    class Media:
        css = {
            'all': ('store/css/my_admin.css',)
        }
        js = ('store/js/my_admin.js',)


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
    search_fields = ['user_name', 'shop_name']


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
        # import pdb
        # pdb.set_trace()
        records = Goods.objects.filter(pk=obj.goods.id)
        if records:
            record = records[0]

            if obj.new_price:
                if obj.new_price == 0:
                    raise ValidationError('修改的价格不能为0')
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
        records = Goods.objects.filter(pk=obj.goods.id)
        if records:
            record = records[0]
            record.remain = record.remain + obj.amount
            record.save()
        else:
            raise ValidationError("库存中还没有这个商品无法进行退送")
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


class ArrearsAdmin(admin.ModelAdmin):
    list_display = ('arrears_price', 'customer', 'is_arrears', 'date')


class GoodsSellRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('customer', 'remark')
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('arrears',)
        }),
    )
    list_display = ('goods', 'sell_num', 'average_price', 'sell_price', 'customer',
                    'arrears', 'remark', 'updater', 'date')
    search_fields = ['goods']

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user

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
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

class OrderAdmin(OrderMixin, admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        categories = Category.objects.all()
        goods = Goods.objects.filter(category=categories[0])
        extra_context = {'categories': categories, 'goods': goods}
        return super(OrderAdmin, self).changelist_view(request, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        return super(OrderAdmin, self).changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(OrderAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def _goods_to_json(self, goods):
        ret = []
        for g in goods:
            data = {}
            data['name'] = g.goods_name
            data['price'] = g.last_price
            data['remain'] = g.remain
            data['unit'] = g.unit_name
            data['id'] = g.id
            ret.append(data)
        return ret

    def search_goods_view(self, request):
        search = request.POST.get('search_text', None)
        if not search:
            return HttpResponse(json.dumps([]), content_type="application/json")
        # goods = Goods.objects.filter(Q(goods_name__icontains=search) | Q(shop__shop_name__icontains=search))
        goods = Goods.objects.filter(Q(goods_name__icontains=search))
        return HttpResponse(json.dumps(self._goods_to_json(goods)), content_type="application/json")

    def search_customer_view(self, request):
        search = request.POST.get('search_text', None)
        if not search:
            return HttpResponse(json.dumps([]), content_type="application/json")
        users = Customer.objects.filter(Q(user_name__icontains=search))
        user_list = []
        for u in users:
            user_dict = {}
            user_dict['name'] = u.user_name
            user_dict['phone'] = u.phone_number
            user_dict['id'] = u.id
            user_list.append(user_dict)
        return HttpResponse(json.dumps(user_list), content_type="application/json")

    def goods_list_view(self, request, cat_id):
        goods = Goods.objects.filter(category=cat_id)
        ret = self._goods_to_json(goods)
        # ret = []
        # for g in goods:
        #     data = {}
        #     data['name'] = g.goods_name
        #     data['price'] = g.last_price
        #     data['remain'] = g.remain
        #     data['unit'] = g.unit_name
        #     data['id'] = g.id
        #     ret.append(data)
        return HttpResponse(json.dumps(ret), content_type="application/json")

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        my_urls = [
            url(r'^goods-list/(\d+)/$',
                self.admin_site.admin_view(self.goods_list_view),
                name='%s_%s_goods-list' % self.get_model_info()),
            url(r'^goods-search-list/$',
                self.admin_site.admin_view(self.search_goods_view),
                name='%s_%s_goods-search-list' % self.get_model_info()),
            url(r'^custom-search-list/$',
                self.admin_site.admin_view(self.search_customer_view),
                name='%s_%s_custom-search-list' % self.get_model_info()),
            url(r'^report/$',
                self.admin_site.admin_view(self.report_view),
                name='%s_%s_report' % self.get_model_info()),
            # url(r'^obj/$',
            #     self.admin_site.admin_view(self.obj_js),
            #     name='%s_%s_obj' % self.get_model_info()),
        ]
        return my_urls + urls


    @transaction.atomic
    def report_view(self, request):
        data = []
        all_price = 0.0
        cell_num = 0  # 增加一些空的行
        code = 1  # 增加一行序号列
        if request.POST.get('data_list', None) is None:
            return HttpResponseRedirect(reverse('admin:index'))
        data_all = json.loads(request.POST['data_list'])
        # prices = data_all['price']
        # for key, value in data_all['num'].items():
        #     g = Goods.objects.get(id=key)
        #     g.num = value
        #     g.code = code
        #     price = float(prices[key])
        #     g.last_price = price
        #     data.append(g)
        #     all_price += value * price
        #     g.remain = g.remain - g.num
        #     g.save()
        #     GoodsSellRecord.objects.create(goods=g, sell_num=value,
        #                                    updater=request.user,
        #                                    average_price=g.average_price,
        #                                    sell_price=price)
        #     cell_num += 1
        #     code += 1
        # import pdb
        # pdb.set_trace()

        arr = data_all['arrears']
        name = data_all['user']
        print(arr, name)

        cust = Customer.objects.get(user_name=name)
        if arr.strip():
            arr = float(arr)
            ap = ArrearsPrice.objects.create(arrears_price=arr, customer=cust)
        else:
            ap = None

        for key, value in data_all['list_data'].items():
            g = Goods.objects.get(id=key)
            g.num = value['num']
            g.code = code
            price = float(value['price'])
            all_price += g.num * price
            g.remain = g.remain - g.num
            g.save()
            # 价格改变只是零时性的
            g.last_price = price
            data.append(g)
            GoodsSellRecord.objects.create(goods=g, sell_num=g.num, updater=request.user,
                                           average_price=g.average_price,
                                           sell_price=price,customer=cust,arrears=ap)
            cell_num += 1
            code += 1


        default_report = Report.objects.filter(tag=True).order_by('-date')[0]


        return render(request, context={'data': data, 'report': default_report, 'price': all_price,
                                        'cell_num': range(max(Max_Row-cell_num, 0))}, template_name=self.report_template)

    # def obj_js(self, request):
    #     self.change_list_template = 'admin/liuzhiping/change_list_obj.html'
    #     categories = Category.objects.all()
    #     goods = Goods.objects.filter(category=categories[0])
    #     extra_context = {'categories': categories, 'goods': goods}
    #     return super(OrderAdmin, self).changelist_view(request, extra_context)

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
admin.site.register(ArrearsPrice, ArrearsAdmin)