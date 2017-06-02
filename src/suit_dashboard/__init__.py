# -*- coding: utf-8 -*-

"""
Django Suit Dashboard package.

Django Suit Dashboard lets you define widgets, and assemble them in your pages
using a Bootstrap-like layout. You can have nested lines and columns.
"""

from .apps import AppSettings
from .layout import Box, Column, Grid, Row
from .urls import get_realtime_urls
from .views import DashboardView
from .widgets import Widget, realtime

__all__ = ['Box', 'Column', 'Grid', 'Row', 'get_realtime_urls', 'realtime',
           'DashboardView', 'Widget', 'AppSettings']

default_app_config = 'suit_dashboard.apps.SuitDashboardConfig'
