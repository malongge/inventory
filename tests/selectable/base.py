from __future__ import unicode_literals

import random
import string
from collections import defaultdict
from xml.dom.minidom import parseString

from bs4 import BeautifulSoup
from django.test import TestCase, override_settings
from selectabletest.models import Thing

from selectable.base import ModelLookup


def as_xml(html):
    "Convert HTML portion to minidom node."
    print(html)
    return parseString('<root>%s</root>' % html)


# def parsed_inputs(html):
#     "Returns a dictionary mapping name --> node of inputs found in the HTML."
#     node = as_xml(html)
#     inputs = {}
#     for field in node.getElementsByTagName('input'):
#         name = dict(field.attributes.items())['name']
#         current = inputs.get(name, [])
#         current.append(field)
#         inputs[name] = current
#     return inputs


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def parsed_inputs(html):
    "Returns a dictionary mapping name --> node of inputs found in the HTML."
    soup = BeautifulSoup(html, 'html.parser')
    inputs = defaultdict(list)
    for field in soup.find_all('input'):
        name = field.get('name')
        obj = Struct(**field.__dict__)

        inputs[name].append(obj)
    return inputs


@override_settings(ROOT_URLCONF='selectable.tests.urls')
class BaseSelectableTestCase(TestCase):
    def get_random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for x in range(length))

    def create_thing(self, data=None):
        data = data or {}
        defaults = {
            'name': self.get_random_string(),
            'description': self.get_random_string(),
        }
        defaults.update(data)
        return Thing.objects.create(**defaults)


class SimpleModelLookup(ModelLookup):
    model = Thing
    search_fields = ('name__icontains',)
