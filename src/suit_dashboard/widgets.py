# -*- coding: utf-8 -*-

"""
Widgets module.

This module provides the Widget class and a realtime method, used to register
a instance of Widget as realtime. The instance has to be registered at
compile time in order for Django to know the URL used to return contents.
"""

from __future__ import unicode_literals

from hashlib import sha256

from .views import PartialResponse

DEFAULT_TIME_INTERVAL = 2000
REALTIME_WIDGETS = []


def realtime(widget, url_name=None, url_regex=None, time_interval=None):
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
            url_name = widget.__name__

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
            time_interval = DEFAULT_TIME_INTERVAL

    class GeneratedView(PartialResponse):
        def get_data(self):
            return widget.get_updated_content()

    GeneratedView.url_name = url_name
    GeneratedView.url_regex = url_regex
    GeneratedView.time_interval = time_interval

    REALTIME_WIDGETS.append(GeneratedView)
    return widget


class Widget(object):
    """Widget class."""
    html_id = None
    name = None
    content = None
    template = ''
    classes = ''

    def __init__(self, html_id=html_id, name=name, content=content,
                 template=template, classes=classes):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML item.
            name (str): the name of the item, displayed in HTML.
            content (): suitable content according to chosen display.
            display (Display): the type of display.
            classes (str): additional classes to pass to the HTML item.
        """
        if html_id != Widget.html_id:
            self.html_id = html_id
        if name != Widget.name:
            self.name = name
        if content != Widget.content:
            self.content = content
        if template != Widget.template:
            self.display = template
        if classes != Widget.classes:
            self.classes = classes

    def get_html_id(self):
        return self.html_id

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

    def get_template(self):
        return self.template

    def get_classes(self):
        return self.classes

    def get_updated_content(self):
        return self.get_content()
