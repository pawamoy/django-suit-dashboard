# -*- coding: utf-8 -*-

"""URL utility to get the URL for the declared refreshable items."""

from __future__ import unicode_literals
from django.conf.urls import url
from suit_dashboard.views import RefreshableDataView


def get_refreshable_urls(admin_view_func=lambda x: x):
    """
    Get the refreshable URL for items that have used the refreshable decorator.

    Args:
        admin_view_func (callable): an admin_view method from an AdminSite
            instance. By default, identity.

    Returns:
        list: the list of the refreshable URLs.
    """
    return [url(c.regex, admin_view_func(c.as_view()), name=c.name)
            for c in RefreshableDataView.children]
