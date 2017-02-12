import json

from django.db.models import Q
from django.http.response import HttpResponse
from django.core import serializers

from .models import Goods, Customer
from .models import Category

from jsonview.views import JSONDetailView, JSONListView, PaginatedJSONListView, JSONListSearchView \
    , PaginatedJSONListSearchView


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
