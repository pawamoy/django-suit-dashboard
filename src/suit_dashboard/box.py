# -*- coding: utf-8 -*-

"""
Box module.

This module provides the Box and Item classes. A box can contain several items,
and each item can be rendered a different way (table, list, highchart).
"""

from __future__ import unicode_literals

import inspect
import json

from suit_dashboard.views import RefreshableDataView


class Box(object):
    """
    Box class.

    A box can be built directly passing values to the constructor. Another way
    you can use it is to create a subclass, and writing a getter for each
    wanted attribute. It will allow the box to be loaded lazily, but also to
    store the values returned by getters in private attributes that can be
    reused later without computing them again.
    """

    html_id = None
    title = None
    description = None
    widgets = None
    template = None
    context = None

    def __init__(self, html_id=html_id, title=title, description=description,
                 widgets=widgets, template=template, context=context):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML box.
            title (str): a title to display on the top of the box.
            description (str): a description to display after the title box.
            items (list): the box's list of items.
            template (str): the path to a custom template to use for this box.
            context (dict): additional context to pass to the box.
            lazy (str): will not load at startup, only when called.
            persistent (str): will store the values of getters into variables.
            **kwargs (): additional attributes to attach to the box itself.
        """
        if widgets:
            if not (isinstance(widgets, list) or isinstance(widgets, tuple)):
                raise AttributeError('Box widgets attribute '
                                     'must be a list or tuple')
            if not all([isinstance(e, Widget) for e in widgets]):
                raise ValueError('All elements of Box must be Widget instances')

        self.type = 'box'

        self.html_id = html_id
        self.title = title
        self.description = description
        self.widgets = widgets
        self.template = template
        self.context = context

    def get_html_id(self):
        return self.html_id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_widgets(self):
        return self.widgets

    def get_template(self):
        return self.template

    def get_context(self):
        return self.context


class Display(object):
    """
    Display class.

    Provide a template path and optionally javascript files paths.
    The template will be used to render a widget in HTML, and the javascript
    files will be included after the template code. These javascript files
    should contain functions to redraw completely or partially update the
    rendered HTML.
    """

    template = None
    javascript = []

    def __init__(self, template=template, javascript=javascript):
        self.template = template
        self.javascript = javascript

    def get_template(self):
        return self.template

    def get_javascript(self):
        return self.javascript


class Widget(object):
    """Widget class."""

    type = 'static_widget'

    html_id = None
    name = None
    content = None
    display = Display()
    classes = ''

    def __init__(self, html_id=html_id, name=name, content=content,
                 display=display, classes=classes):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML item.
            name (str): the name of the item, displayed in HTML.
            content (): suitable content according to chosen display.
            display (Display): the type of display.
            classes (str): additional classes to pass to the HTML item.
        """
        self.html_id = html_id
        self.name = name
        self.content = content
        self.display = display
        self.classes = classes

    def get_html_id(self):
        return self.html_id

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

    def get_display(self):
        return self.display

    def get_classes(self):
        return self.classes


class StaticWidget(Widget):
    pass


class RealTimeWidget(Widget):
    type = 'real_time_widget'

    def get_updated_content(self):
        raise NotImplementedError(
            'get_updated_content for object %s is not implemented' % self)
