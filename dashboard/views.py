# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from suit_dashboard.layout import Grid, Row, Column
from suit_dashboard.views import DashboardView
from suit_dashboard.box import Box
from .box import BoxMachine


class HomeView(DashboardView):
    template_name = 'dashboard/main.html'

    crumbs = (
        {'url': 'admin:statistics', 'name': '统计信息'},
    )
    grid = Grid(Row(Column(BoxMachine(), width=6)))

    # template_name = 'dashboard/main.html'
    #
    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context=context)


class SellGoodsView(DashboardView):
    template_name = 'dashboard/sells.html'

    crumbs = (
        {'url': 'admin:sells', 'name': '下订单'},
    )

    grid = Grid()


# inheriting home view
class LogsMenu(HomeView):
    crumbs = (
        {'url': 'admin:logs', 'name': 'Logs analysis'},
    )
    grid = Grid(
        Row(
            Column(
                Box(title='Row 1 column 1 box 1'),
                Box(title='Row 1 column 1 box 2'),
                width=6),
            Column(
                Box(title='Row 1 column 2 box 1'),
                Box(title='Row 1 column 2 box 2'),
                width=6),
        ),
        Row(
            Column(
                Box(title='Row 2 column 1 box 1'),
                Box(title='Row 2 column 1 box 2'),
                width=3),
            Column(
                Box(title='Row 2 column 2 box 1'),
                Box(title='Row 2 column 2 box 2'),
                width=5),
            Column(
                Row(
                    Column(
                        Box(title='R2 C3 R1 C1 B1'),
                        Box(title='R2 C3 R1 C1 B2'),
                        width=12)
                ),
                Row(
                    Column(
                        Box(title='R2 C3 R2 C1 B1'),
                        Box(title='R2 C3 R2 C1 B2'),
                        width=12)
                ),
                width=4),
        )
    )
