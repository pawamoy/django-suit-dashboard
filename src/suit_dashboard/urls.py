# -*- coding: utf-8 -*-

"""URL utility to get the URL for the declared refreshable items."""

from __future__ import unicode_literals
from django.conf.urls import url


def get_realtime_urls(admin_view_func=lambda x: x):
    """
    Get the refreshable URL for items that have used the refreshable decorator.

    Args:
        admin_view_func (callable): an admin_view method from an AdminSite
            instance. By default, identity.

    Returns:
        list: the list of the refreshable URLs.
    """
    from .admin import REALTIME_WIDGETS
    return [url(w.url_regex, admin_view_func(w.as_view()), name=w.url_name)
            for w in REALTIME_WIDGETS]
