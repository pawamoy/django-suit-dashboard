# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random
import string
from suit_dashboard.views import RefreshableDataView


def refreshable(func, name=None, regex=None, refresh_time=5000):
    if name is None:
        name = func.__name__

    if name in [c.name for c in RefreshableDataView.children]:
        raise ValueError('Name %s is already used by another '
                         'RefreshableDataView subclass.' % name)

    if regex is None:
        while True:
            regex = ''.join(random.SystemRandom().choice(
                string.ascii_lowercase + string.digits) for _ in range(32))
            if regex not in [c.regex for c in RefreshableDataView.children]:
                break

    def inner_function(*args, **kwargs):
        class InnerClass(RefreshableDataView):
            def get_data(self):
                return func(*args, **kwargs)

        InnerClass.name = name
        InnerClass.regex = regex
        InnerClass.refresh_time = refresh_time

        RefreshableDataView.children.append(InnerClass)

        return InnerClass
    return inner_function
