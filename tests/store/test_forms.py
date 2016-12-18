import pytest

from store.forms import AddRecordAdminForm, ReturnRecordForm
from store.models import Goods, Category, Shop
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestAdminForm:

    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        updater = User.objects.create(username='tester', password='123456')
        category = Category.objects.create(name='洗衣机配件')
        goods = Goods.objects.create(
            goods_name='test',
            average_price=2,
            last_price=4,
            unit_name='个',
            updater=updater,
            remain=2
        )
        self.goods = goods
        goods.category.add(category)
        Shop.objects.create(user_name='张三', shop_name='湖南批发市场', shop_address='长沙', phone_number='07997945')

    def test_form_without_new_price(self):
        form_data = {
            'goods': 1,
            'number': 1,
            'shop': 1,
            'updater': 1
        }
        form = AddRecordAdminForm(form_data)
        form.is_valid()
        assert bool(form.errors) is False
        assert form.cleaned_data['new_goods'].average_price == 2
        assert form.cleaned_data['new_goods'].remain == 3

    def test_form_with_new_price(self):
        form_data = {
            'goods': 1,
            'number': 2,
            'shop': 1,
            'updater': 1,
            'new_price': 4
        }
        form = AddRecordAdminForm(form_data)
        form.is_valid()
        assert bool(form.errors) is False
        assert form.cleaned_data['new_goods'].average_price == 3
        assert form.cleaned_data['new_goods'].remain == 4

    def test_return_record_form(self):
        form_data = {
            'goods': 1,
            'shop': 1,
            'amount': 1,
            'type': 0,
            'updater': 1,
        }
        form = ReturnRecordForm(form_data)
        form.is_valid()
        assert form.cleaned_data['new_goods'].remain == 3
        assert form.cleaned_data['new_goods'].average_price == 2

    def test_return_record_form_new_price(self):
        form_data = {
            'goods': 1,
            'shop': 1,
            'amount': 1,
            'type': 0,
            'updater': 1,
            'reset_price': 4
        }
        form = ReturnRecordForm(form_data)
        form.is_valid()
        assert form.cleaned_data['new_goods'].remain == 3
        assert form.cleaned_data['new_goods'].average_price == 4

    def test_add_record_form_save(self):
        form_data = {
            'goods': 1,
            'number': 1,
            'shop': 1,
            'updater': 1
        }
        form = AddRecordAdminForm(form_data)
        form.is_valid()
        obj = form.save()
        assert obj.goods == self.goods

    def test_new_price_is_zero(self):
        form_data = {
            'goods': 1,
            'number': 1,
            'shop': 1,
            'updater': 1,
            'new_price': 0
        }
        form = AddRecordAdminForm(form_data)
        form.is_valid()
        assert form.errors['__all__'][0] == 'new price can not be zero'

    def test_goods_not_exist(self):
        form_data = {
            'goods': 2,
            'number': 1,
            'shop': 1,
            'updater': 1,
        }
        form = AddRecordAdminForm(form_data)
        form.is_valid()
        assert form.errors['__all__'][0] == 'goods have not exist in store, please first add it'

