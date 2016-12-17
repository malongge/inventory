from django.contrib import admin
from django.contrib.admin import register
from django.core.exceptions import ValidationError
from django.db import transaction

from store.forms import AddRecordAdminForm
from .models import (Goods, Customer, Category,
                     GoodsAddRecord, GoodsSellRecord, Shop,
                     ArrearsPrice, TransferGoods, Report,
                     Order, ReturnRecord)


@register(Goods)
class GoodsAdmin(admin.ModelAdmin):

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
        'goods_name', 'unit_name', 'average_price', 'last_price',
        'remain', 'sell_amount', 'in_amount', 'own_amount',
        'last_time', 'add_people', 'update_date')

    list_filter = ['category']

    search_fields = ['goods_name']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'add_people', None) is None:
            obj.add_people = request.user

        obj.save()

    class Media:
        css = {
            'all': ('store/css/my_admin.css',)
        }
        js = ('store/js/my_admin.js',)


@register(Customer)
class CustomsAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('user_name', 'address', 'phone_number',)
        }),
    )

    list_display = ('user_name', 'address', 'phone_number',)

    search_fields = ['user_name']


@register(Category)
class CategoryAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'remark', 'super_category')
        }),
    )

    list_display = ('name', 'remark', 'super_category', 'add_date',)

    search_fields = ['name']


@register(Shop)
class ShopAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('user_name', 'shop_name', 'phone_number', 'shop_address',)
        }),
    )
    list_display = ('user_name', 'shop_name', 'phone_number', 'shop_address', 'add_date',)

    search_fields = ['user_name', 'shop_name']


@register(GoodsAddRecord)
class GoodsAddRecordAdmin(admin.ModelAdmin):

    form = AddRecordAdminForm

    fieldsets = (
        (None, {
            'fields': ('goods', 'shop', 'number',)
        }),
        ('选填项', {
            'classes': ('collapse',),
            'fields': ('remark', 'new_price')
        }),
    )
    list_display = ('goods', 'shop', 'number', 'remark', 'updater', 'date', 'new_price')

    search_fields = ['goods__goods_name', 'shop']

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user
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


@register(ReturnRecord)
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

    search_fields = ['goods__goods_name', 'shop']

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


@register(TransferGoods)
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
    list_display = (
    'goods', 'from_shop', 'to_shop', 'from_price', 'to_price', 'change_num', 'remark', 'updater', 'date')
    search_fields = ['goods__goods_name', 'from_shop', 'to_shop']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user

        obj.save()


@register(ArrearsPrice)
class ArrearsAdmin(admin.ModelAdmin):
    list_display = ('arrears_price', 'customer', 'is_arrears', 'date')

from django.utils.safestring import mark_safe
@register(GoodsSellRecord)
class GoodsSellRecordAdmin(admin.ModelAdmin):

    list_display = ('goods', 'sell_num', 'sell_price', 'customer',
                    'arrears', 'available_data', 'remark', 'date', )
    search_fields = ['goods__goods_name', 'customer__user_name']

    list_filter = ['date']

    class Media:
        css = {
            'all': ('store/css/price_admin.css',)
        }
        js = ('store/js/price_admin.js',)

    def available_data(self, obj):
        month_string = mark_safe('<a href="javascript:void(0)" class="show-price">查看进价<em style="display:none">' + str(
            obj.average_price) + '</em></a>')
        return month_string

    available_data.short_description = '操作项'

    available_data.allow_tags = True

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'updater', None) is None:
            obj.updater = request.user

        obj.save()


class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'alias', 'ad', 'phone', 'address', 'remark', 'date',
                    'tag')

    search_fields = ['title', 'alias', 'remark']


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


from django.conf.urls import url
from django.http.response import HttpResponse
from django.shortcuts import render
import json
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q


@register(Order)
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
            data['price'] = str(g.last_price)
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
                                           sell_price=price, customer=cust, arrears=ap)
            cell_num += 1
            code += 1

        default_report = Report.objects.filter(tag=True).order_by('-date')[0]

        if ap:
            arr_p = ap.arrears_price
        else:
            arr_p = 0
        return render(request, context={'data': data, 'report': default_report, 'price': all_price, 'customer': cust,
                                        'arrears': arr_p,
                                        'cell_num': range(max(13 - cell_num, 0))},
                      template_name=self.report_template)

