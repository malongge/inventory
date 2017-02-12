from django.conf.urls import url
from .views import search_customer_view, search_goods_view, goods_list_view
from .views import GoodsJson,test_objects, GoodsListJson, GoodsPaginatedJSONListView,GoodsSearchJSONListView
urlpatterns = [
    url(r'^search-goods$', search_goods_view, name='search_goods'),
    url(r'^search-customers$', search_customer_view, name='search_customers'),
    url(r'^filter-by-cate$', goods_list_view, name='filter_goods_by_category'),
    url(r'json', GoodsJson.as_view()),
    url(r'search', GoodsSearchJSONListView.as_view()),
    url(r'objects', test_objects)
]
