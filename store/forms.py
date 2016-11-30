from django import forms
import selectable.forms as selectable
from store.models import GoodsAddRecord,Goods

from selectable.base import ModelLookup
from selectable.registry import registry


class AddRecordLookup(ModelLookup):
    model = Goods
    search_fields = ('goods_name__icontains', )

registry.register(AddRecordLookup)


class AddRecordAdminForm(forms.ModelForm):
    goods = selectable.AutoCompleteSelectField(lookup_class=AddRecordLookup, allow_new=False)

    class Meta(object):
        model = GoodsAddRecord
        exclude = ('goods', )

    def __init__(self, *args, **kwargs):
        super(AddRecordAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.goods:
            self.initial['goods'] = self.instance.goods.pk

    def save(self, *args, **kwargs):
        goods = self.cleaned_data['goods']
        # if goods and not owner.pk:
        #     owner = User.objects.create_user(username=owner.username, email='')
        self.instance.goods = goods
        return super(AddRecordAdminForm, self).save(*args, **kwargs)
from searchableselect.widgets import SearchableSelect

class GoodsAdminForm(forms.ModelForm):
    class Meta:
        model = Goods
        exclude = ()
        widgets = {
            'category': SearchableSelect(model='store.Category', search_field='name', many=True)
        }