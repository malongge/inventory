from django.core import serializers
from store.models import Category
import json
import pytest


@pytest.mark.django_db
class TestAliasJSONSerializer:

    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        self.cate = Category.objects.create(name='洗衣机配件')

    def test_serializer_with_id(self):
        data = serializers.serialize('alias_json', [self.cate])
        data = json.loads(data)
        data = data[0]
        assert 'id' in data
        assert data['id'] == 1

    def test_serializer_with_alias(self):
        data = serializers.serialize(
            'alias_json',
            [self.cate],
            fields=('id', 'name'),
            alias={'id': 'pk', 'name': 'cname'})
        assert json.loads(data) == [{'pk': 1, 'cname': '洗衣机配件'}]