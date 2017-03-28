# -*- coding: utf-8 -*-

"""App module providing the application settings class."""
from django.apps import AppConfig
from django.conf import settings


class SuitDashboardConfig(AppConfig):
    name = 'suit_dashboard'
    verbose_name = 'Suit Dashboard'

    def ready(self):
        AppSettings.check()


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
