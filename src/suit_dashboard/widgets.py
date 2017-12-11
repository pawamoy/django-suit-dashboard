# -*- coding: utf-8 -*-

"""
Widgets module.

This module provides the Widget class and a real-time method, used to register
a instance of Widget as real-time. The instance has to be registered at
compile time in order for Django to know the URL used to return contents.
"""

from __future__ import unicode_literals

from hashlib import sha256

from .apps import AppSettings

app_settings = AppSettings()

REALTIME_WIDGETS = []


def realtime(widget, url_name=None, url_regex=None, time_interval=None):
    """
    Return a widget as real-time.

    Args:
        widget (Widget): the widget to register and return as real-time.
        url_name (str): the URL name to call to get updated content.
        url_regex (regex): the URL regex to be matched.
        time_interval (int): the interval of refreshment in milliseconds.

    Returns:
        Widget: the "real-timed" widget.
    """
    if not hasattr(widget, 'get_updated_content'):
        raise AttributeError('Widget %s must implement get_updated_content '
                             'method.' % widget)
    elif not callable(widget.get_updated_content):
        raise ValueError('get_updated_content in widget %s is not callable'
                         % widget)

    if url_name is None:
        if getattr(widget, 'url_name', None) is not None:
            url_name = widget.url_name
        else:
            url_name = widget.__class__.__name__

    if url_name in [w.url_name for w in REALTIME_WIDGETS]:
        raise ValueError('URL name %s is already used by another '
                         'real time widget.' % url_name)

    if url_regex is None:
        if getattr(widget, 'url_regex', None) is not None:
            url_regex = widget.url_regex
        else:
            url_regex = sha256(url_name.encode('utf-8'))
            url_regex = url_regex.hexdigest()[:32]
            url_regex = 'realtime/' + url_regex

    if url_regex in [w.url_regex for w in REALTIME_WIDGETS]:
        raise ValueError('URL regex %s is already used by another '
                         'real time widget.' % url_regex)

    if time_interval is None:
        if getattr(widget, 'time_interval', None) is not None:
            time_interval = widget.time_interval
        else:
            time_interval = app_settings.default_time_interval

    from django.views.generic import View
    from braces.views import AjaxResponseMixin, JSONResponseMixin

    # pylama:ignore=C0111,R0201
    class PartialResponse(JSONResponseMixin, AjaxResponseMixin, View):
        def get_data(self):
            return widget.get_updated_content()

        def get(self, request, *args, **kwargs):
            return self.get_ajax(request, *args, **kwargs)

        def get_ajax(self, request, *args, **kwargs):
            return self.render_json_response(self.get_data())

    PartialResponse.url_name = url_name
    PartialResponse.url_regex = url_regex
    PartialResponse.time_interval = time_interval

    REALTIME_WIDGETS.append(PartialResponse)

    if not hasattr(widget, 'url_name'):
        widget.url_name = url_name
    if not hasattr(widget, 'url_regex'):
        widget.url_regex = url_regex
    if not hasattr(widget, 'time_interval'):
        widget.time_interval = time_interval

    return widget


class Widget(object):
    """Widget class."""

    def __init__(self,
                 html_id=None,
                 name=None,
                 content=None,
                 template=None,
                 classes=None,
                 **kwargs):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML item.
            name (str): the name of the item, displayed in HTML.
            content (): suitable content according to chosen display.
            template (str): the template responsible for display.
            classes (str): additional classes to pass to the HTML item.
        """
        if html_id is not None:
            try:
                self.html_id = html_id
            except AttributeError:
                self._html_id = html_id
        if name is not None:
            try:
                self.name = name
            except AttributeError:
                self._name = name
        if content is not None:
            try:
                self.content = content
            except AttributeError:
                self._content = content
        if template is not None:
            try:
                self.template = template
            except AttributeError:
                self._template = template
        if classes is not None:
            try:
                self.classes = classes
            except AttributeError:
                self._classes = classes

        if not hasattr(self, 'template'):
            raise AttributeError('template is a required widget attribute')

        for kw, arg in kwargs.items():
            setattr(self, kw, arg)

    def get_updated_content(self):
        """Return updated content (for real-time widgets)."""
        return self.content
