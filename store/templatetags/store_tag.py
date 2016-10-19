#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Created by malongge on 2016/10/18
#

from __future__ import unicode_literals
import datetime
from django import template
import logging

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag(name="my_time")
def current_time():
    return datetime.datetime.now().strftime('%Y{}%m{}%d{}').format('年', '月', '日')


@register.filter(name='new_line')
def replace_new_line(value):
    return value.replace('\n', ' <br> ')
