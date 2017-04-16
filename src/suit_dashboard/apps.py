# -*- coding: utf-8 -*-

"""App module providing the application settings class."""
from django.apps import AppConfig

import appsettings as aps


class SuitDashboardConfig(AppConfig):
    name = 'suit_dashboard'
    verbose_name = 'Suit Dashboard'

    def ready(self):
        AppSettings.check()


class AppSettings(aps.AppSettings):
    """
    Application settings class.

    Settings:
    - default_time_interval (int)
    """

    default_time_interval = aps.PositiveIntSetting(default=1000)

    class Meta:
        setting_prefix = 'SUIT_DASH_'
