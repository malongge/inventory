# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from suit_dashboard.box import Box
from suit_dashboard.layout import Grid, Row, Column
from suit_dashboard.views import DashboardView
from .box import BoxSellStatistics, DaySellStatistics


class HomeView(DashboardView):
    template_name = 'dashboard/main.html'

    crumbs = (
        {'url': 'admin:statistics', 'name': '统计信息'},
    )
    current_year = str(datetime.now())[:4]
    last_year = str(int(current_year) - 1)
    grid = Grid(Row(Column(BoxSellStatistics(year=current_year), width=6),
                    Column(DaySellStatistics(year=current_year), width=6)),
                Row(Column(BoxSellStatistics(year=last_year), width=6),
                    Column(DaySellStatistics(year=last_year), width=6)))

    # template_name = 'dashboard/main.html'
    #
    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context=context)


from store.models import Category, Goods


class SellGoodsView(DashboardView):
    template_name = 'dashboard/sells.html'

    crumbs = (
        {'url': 'admin:sells', 'name': '下订单'},
    )

    # extra_context = {'categories': Category.objects.all(), 'goods': }

    grid = Grid(Row(Column(
        Box(template='record/search.html'), width=12
    )), Row(
        Column(
            Box(template='record/category.html'),
            width=2),
        Column(
            Box(template='record/goods.html'),
            width=6),
        Column(
            Box(template='record/record.html'),
            width=4),
    ))

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        goods = Goods.objects.filter(category=categories[0])
        context = super(SellGoodsView, self).get_context_data(**kwargs) or {}
        context.update({'categories': categories, 'goods': goods})
        return context


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
