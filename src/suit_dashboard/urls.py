# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from suit_dashboard.views import RefreshableDataView


def get_refreshable_urls(admin_view_func=lambda x: x):
    return [url(c.regex, admin_view_func(c.as_view()), name=c.name)
            for c in RefreshableDataView.children]
