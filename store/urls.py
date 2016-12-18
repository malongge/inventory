from django.conf.urls import url
from .views import goods_json

urlpatterns = [
    url(r'^(?P<pk>\d+)$', goods_json),

]