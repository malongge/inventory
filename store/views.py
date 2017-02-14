import json

from django.core import serializers
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render

from jsonview.views import JSONDetailView, JSONListView, PaginatedJSONListView, PaginatedJSONListSearchView
from .models import Category, RecordHistory
from .models import Goods, Customer

from decimal import Decimal
def view_record(request, record_id):
    record = RecordHistory.objects.get(id=record_id)
    for sell_rcord in record.report_many_record.all():
        print(sell_rcord.sell_num)

    data = []
    all_price = Decimal(0)
    cell_num = 0  # 增加一些空的行
    code = 1  # 增加一行序号列

    cust = record.customer
    default_report = record.report
    for sell_record in record.report_many_record.all():
        g = sell_record.goods
        g.code = code
        g.num = sell_record.sell_num
        all_price += g.count
        # 价格改变只是零时性的
        g.last_price = sell_record.sell_price
        data.append(g)

        cell_num += 1
        code += 1

    ap = record.arrears if record.arrears else 0

    return render(request, context={'data': data, 'report': default_report, 'price': all_price, 'customer': cust,
                                    'arrears': ap,
                                    'cell_num': range(max(13 - cell_num, 0)), 'my_time': record.date.strftime('%Y{}%m{}%d{}').format('年', '月', '日')},
                  template_name='admin/liuzhiping/report.html')


def _get_goods_serialize(goods):
    return serializers.serialize("alias_json",
                                 goods,
                                 fields=('id', 'goods_name', 'last_price', 'remain', 'unit_name'),
                                 alias={'goods_name': 'name', 'last_price': 'price', 'unit_name': 'unit'}
                                 )


def _get_user_serialize(users):
    return serializers.serialize("alias_json",
                                 users,
                                 fields=('id', 'user_name', 'phone_number'),
                                 alias={'user_name': 'name', 'phone_number': 'phone'}
                                 )


def search_goods_view(request):
    search = request.GET.get('search_text', None)
    if not search:
        return HttpResponse(json.dumps([]), content_type="application/json")
    # goods = Goods.objects.filter(Q(goods_name__icontains=search) | Q(shop__shop_name__icontains=search))
    goods = Goods.objects.filter(Q(goods_name__icontains=search))
    return HttpResponse(_get_goods_serialize(goods), content_type="application/json")


def search_customer_view(request):
    search = request.GET.get('search_text', None)
    if not search:
        return HttpResponse(json.dumps([]), content_type="application/json")
    users = Customer.objects.filter(Q(user_name__icontains=search))
    return HttpResponse(_get_user_serialize(users), content_type="application/json")


def goods_list_view(request, cat_id):
    goods = Goods.objects.filter(category=cat_id)
    return HttpResponse(_get_goods_serialize(goods), content_type="application/json")


class GoodsJson(JSONDetailView):
    model = Goods
    # serialize_use_natural_foreign_keys = True
    # serialize_fields = ['remain', 'unit_name']
    serialize_alias_filed = {'remain': 'last'}
    serialize_mtm = True
    serialize_mto = True


class GoodsListJson(JSONListView):
    model = Goods


class GoodsPaginatedJSONListView(PaginatedJSONListView):
    model = Goods
    serialize_mtm = True
    serialize_mto = True


class GoodsSearchJSONListView(PaginatedJSONListSearchView):
    model = Category
    search_text = None
    serialize_mtm = True
    serialize_mto = True
    # count_only = True


def test_objects(request):
    from .models import GoodsSellRecord
    import json
    data = GoodsSellRecord.statistic_objects.month_statistic('2016')
    # data = GoodsSellRecord.statistic_objects.year_statistic()
    return HttpResponse(json.dumps(data))
