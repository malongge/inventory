from django import forms
from django.core.exceptions import ValidationError

import selectable.forms as selectable
from selectable.base import ModelLookup
from selectable.registry import registry
from store.models import GoodsAddRecord, Goods, ReturnRecord


class GoodsLookup(ModelLookup):
    model = Goods
    search_fields = ('goods_name__icontains',)


registry.register(GoodsLookup)


class UseSearchGoodsForm(forms.ModelForm):
    goods = selectable.AutoCompleteSelectField(lookup_class=GoodsLookup, allow_new=False, label='商品')

    def __init__(self, *args, **kwargs):
        super(UseSearchGoodsForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.goods:
            self.initial['goods'] = self.instance.goods.pk

    def clean(self):
        data = self.cleaned_data
        if not data.get('goods', None):
            raise ValidationError('请先选择一个商品进行操作')
        self._other_check(data)
        return super(UseSearchGoodsForm, self).clean()

    def _other_check(self, data):
        pass

    def save(self, *args, **kwargs):
        goods = self.cleaned_data['goods']
        self.instance.goods = goods
        return super(UseSearchGoodsForm, self).save(*args, **kwargs)


class AddRecordAdminForm(UseSearchGoodsForm):
    class Meta(object):
        model = GoodsAddRecord
        exclude = ('goods',)

    # def __init__(self, *args, **kwargs):
    #     super(AddRecordAdminForm, self).__init__(*args, **kwargs)
    #     if self.instance and self.instance.pk and self.instance.goods:
    #         self.initial['goods'] = self.instance.goods.pk

    def _other_check(self, data):
        g = data['goods']
        new_price = data.get('new_price', None)

        if new_price is not None:
            if new_price <= 0:
                raise ValidationError('new price can not be zero')
            else:
                # 新的平均价格为 新增加数量的货物总价 + 加上原来的货物总价 / 剩余数量和增加数量
                g.average_price = (new_price * data['number'] + g.remain * g.average_price) \
                                  / (g.remain + data['number'])

        g.remain = g.remain + data['number']
        self.cleaned_data['new_goods'] = g

        # def save(self, *args, **kwargs):
        #     goods = self.cleaned_data['goods']
        #     self.instance.goods = goods
        #     return super(AddRecordAdminForm, self).save(*args, **kwargs)
        #


class ReturnRecordForm(UseSearchGoodsForm):
    class Meta(object):
        model = ReturnRecord
        exclude = ('goods',)

    def _other_check(self, data):
        print(data)
        g = data['goods']
        g.remain = g.remain + data['amount']
        if data.get('reset_price', None) and data.get('reset_price') > 0:
            g.average_price = data['reset_price']
        self.cleaned_data['new_goods'] = g
