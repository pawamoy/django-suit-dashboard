# -*- coding: utf-8 -*-

"""App module providing the application settings class."""

from django.apps import AppConfig

import appsettings as aps


class SuitDashboardConfig(AppConfig):
    """Django application configuration."""

    name = 'suit_dashboard'
    verbose_name = 'Suit Dashboard'

    # pylama:ignore=R0201,C0111
    def ready(self):
        AppSettings.check()


class AppSettings(aps.AppSettings):
    """
    Application settings class.

    Settings:
    - default_time_interval (int)
    """

    default_time_interval = aps.PositiveIntegerSetting(default=1000)

    # pylama:ignore=C0111
    class Meta:
        setting_prefix = 'SUIT_DASH_'
