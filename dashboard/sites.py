# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.admin.sites import AdminSite
from django.conf.urls import url
from dashboard.views import HomeView, LogsMenu, SellGoodsView


# class AdminMixin(object):
#     """Mixin for AdminSite to allow custom dashboard views."""
#
#     def get_urls(self):
#         """Add dashboard view to admin urlconf."""
#         urls = super(DashboardSite, self).get_urls()
#         custom_urls = [
#             url(r'^$', self.admin_view(HomeView.as_view()), name='index')
#         ]
#
#         del urls[0]
#         return custom_urls + urls
#


class DashboardSite(AdminSite):
    """
    A Django AdminSite with the AdminMixin to allow registering custom
    dashboard view.
    """
    def get_urls(self):
        """Add dashboard view to admin urlconf."""
        urls = super(DashboardSite, self).get_urls()
        custom_urls = [
            url(r'^statistics$', self.admin_view(HomeView.as_view()), name='statistics$'),
            url(r'^sells$', self.admin_view(SellGoodsView.as_view()), name='sells')
        ]

        # del urls[0]
        return custom_urls + urls