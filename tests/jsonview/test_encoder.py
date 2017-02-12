#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests.encoding_tests
# Encoding test to deal with issue #11
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Mar 11 09:32:12 2015 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: encoding_tests.py [] benjamin@bengfort.com $

"""
Encoding test to deal with issue #11
"""

##########################################################################
## Imports
##########################################################################

from django.test import TestCase, RequestFactory
from tests.jsonview.jsonviewtest.models import NoForeignKeyModel
from jsonview.encoder import dumps
import json


class TestEncoding(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.context = {'flag': 1}

    def test_no_foreignkey_serialize(self):
        m = NoForeignKeyModel.objects.create(name='thomas')
        self.context.update({'obj': m})
        assert json.loads(dumps(self.context)) == {'flag': 1, 'obj': {'id': 1, 'name': 'thomas'}}


        # def test_encoding(self):
        #     """
        #     Ensure that the response has the correct encoding
        #     """
        #
        #     request = self.factory.get('/', content_type='application/json')
        #     response = self.view(request)
        #     self.assertEqual(response.status_code, 200)
        #
        #     # Check the content type for the charset
        #     self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
