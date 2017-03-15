# -*- coding: utf-8 -*-

"""
Django Suit Dashboard package.

Django Suit Dashboard works on top of Suit, an enhanced admin interface for
Django projects. It lets you define boxes (widgets), and assemble them in your
pages using a Bootstrap-like layout. You can have nested lines and columns.
"""

from django.conf import settings

__version__ = '1.0.3'


class AppSettings(object):
    """
    Application settings class.

    This class provides static getters for each setting, and also an instance
    ``load`` method to load every setting in an instance.
    """

    def __init__(self):
        """Init method."""
        self.default_time_interval = None

    def load(self):
        """Load every settings in self."""
        self.default_time_interval = AppSettings.get_default_time_interval()

    @staticmethod
    def get_default_time_interval():
        """Return default time interval value."""
        return getattr(settings, 'SUIT_DASH_DEFAULT_TIME_INTERVAL', 1000)
