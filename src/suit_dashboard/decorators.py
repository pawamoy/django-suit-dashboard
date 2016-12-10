# -*- coding: utf-8 -*-

"""
Decorators.

A handy double wrap decorator to create decorators that can be used in both
ways: with parameters or without.

The refreshable decorator, used for functions that return some data to be used
in items.
"""

from __future__ import unicode_literals

from functools import wraps
from hashlib import sha256

from suit_dashboard.views import RefreshableDataView


# https://stackoverflow.com/questions/653368/
def double_wrap(f):
    """
    Double wrap decorator to build developer-friendly decorators.

    Args:
        f (callable): the function to decorate.

    Returns:
        callable: the decorated function.
    """
    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return f(args[0])
        else:
            return lambda real_f: f(real_f, *args, **kwargs)

    return new_dec


@double_wrap
def refreshable(func, name=None, regex=None, refresh_time=5000):
    """
    Refreshable decorator.

    The purpose is to make possible the creation of items in boxes that will
    auto-refresh themselves with JSON calls. Very useful for highcharts items.

    Args:
        func: the function that returns the data to be refreshed.
        name: the name of the URL for Django's url function.
        regex: the regex used to build the URL for the JSON call.
        refresh_time: the interval in milliseconds for refreshing.

    Returns:
        callable: a function that will return a RefreshableDataView class.
    """
    if name is None:
        name = func.__name__

    if name in [c.name for c in RefreshableDataView.children]:
        raise ValueError('Name %s is already used by another '
                         'RefreshableDataView subclass.' % name)

    # NOTE: apparently the functions are GC'd, and therefore their memory
    # address change over time. The last solution I see to have "secure" urls,
    # or at least "non-guessable" urls, is to hash the function name, which
    # does not change over time.
    if regex is None:
        regex = sha256(name.encode('utf-8'))
        # regex = sha256(str(id(func)))  # Would just id be sufficient?
        regex = regex.hexdigest()[:32]
        while True:
            # regex = 'refreshable/' + ''.join(random.SystemRandom().choice(
            #     string.ascii_lowercase + string.digits) for _ in range(32))
            regex = 'refreshable/' + regex
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
