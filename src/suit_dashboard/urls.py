# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from suit_dashboard.views import RefreshableDataView


def get_refreshable_urls(admin_view_func=lambda x: x):
    return [url(i.regex, admin_view_func(i.as_view()), i.name)
            for i in RefreshableDataView.instances]
