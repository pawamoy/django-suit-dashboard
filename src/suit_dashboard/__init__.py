# -*- coding: utf-8 -*-

"""
Django Suit Dashboard package.

Django Suit Dashboard lets you define widgets, and assemble them in your pages
using a Bootstrap-like layout. You can have nested lines and columns.
"""

from django.conf import settings

__version__ = '2.0.0'


class AppSettings(object):
    """
    Application settings class.

    This class provides static getters and checkers for each setting, and also
    an instance ``load`` method to load every setting in an instance. The
    static ``check`` method will run the checks against all settings.
    """

    def __init__(self):
        """Init method."""
        self.default_time_interval = None

    def load(self):
        """Load every settings in self."""
        self.default_time_interval = AppSettings.get_default_time_interval()

    @staticmethod
    def check():
        """Run every check method for settings."""
        AppSettings.check_default_time_interval()

    @staticmethod
    def check_default_time_interval():
        """Check the value of given time interval setting."""
        default_time_interval = AppSettings.get_default_time_interval()
        if not isinstance(default_time_interval, int):
            raise ValueError('DEFAULT_TIME_INTERVAL must be int')
        elif default_time_interval < 0:
            raise ValueError('DEFAULT_TIME_INTERVAL must be positive or zero')

    @staticmethod
    def get_default_time_interval():
        """Return default time interval value."""
        return getattr(settings, 'SUIT_DASH_DEFAULT_TIME_INTERVAL', 1000)


AppSettings.check()
