# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from suit_dashboard.views import RefreshableDataView


def refreshable(name=None, regex=None):
    def wrap(func):
        if name is None:
            return RefreshableDataView(func, func.__name__, regex)
        return RefreshableDataView(func, name, regex)
    return wrap
