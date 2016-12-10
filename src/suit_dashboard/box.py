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

    def __init__(self, html_id=None, title=None, description=None,
                 items=None, template=None, context=None,
                 lazy=False, persistent=False, **kwargs):
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
        if items:
            if not (isinstance(items, list) or isinstance(items, tuple)):
                raise AttributeError('Box items attribute '
                                     'must be a list or tuple')
            if not all([isinstance(e, Item) for e in items]):
                raise ValueError('All elements of Box must be Item instances')

        self.type = 'box'
        one_shot = persistent and not lazy
        self.lazy = lazy
        self.persistent = persistent
        self.one_shot = one_shot

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        local = locals()
        for attr, default in {
            'html_id': '',
            'title': '',
            'description': '',
            'items': [],
            'template': '',
            'context': {},
        }.items():
            private = '_%s' % attr
            getter = 'get_%s' % attr
            if not hasattr(self, getter):
                setattr(self, getter, self._getter(default))
            setattr(self.__class__, attr, self._property(private, getter))
            if local[attr]:
                setattr(self, private, local[attr])
            elif one_shot:
                setattr(self, private, getattr(self, getter)())

    def _getter(self, default):
        return lambda: default

    def _property(self, private, getter_name):
        def getter(self):
            if not hasattr(self, private):
                if self.persistent:
                    setattr(self, private, getattr(self, getter_name)())
                    return getattr(self, private)
                return getattr(self, getter_name)()
            return getattr(self, private)

        return property(fget=getter)


class Item(object):
    """
    Item class.

    Attributes:
        AS_TABLE (str): display item as table.
        AS_LIST (str): display item as list.
        AS_HIGHCHARTS (str): display item as highchart.
    """

    AS_TABLE = 'table'
    AS_LIST = 'list'
    AS_HIGHCHARTS = 'highcharts'

    def __init__(self, html_id=None, name=None, value=None,
                 display=None, template=None, classes=''):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML item.
            name (str): the name of the item, displayed in HTML.
            value (str/list/dict): a string, a list, a nested list (2-dim array
                for tables) or a dict for highcharts.
            display (str): the type of display.
            template (str): the path to a custom template to use for this item.
            classes (str): additional classes to pass to the HTML item.
        """
        self.type = 'item'
        self.html_id = html_id
        self.name = name
        if display == Item.AS_HIGHCHARTS:
            if (inspect.isclass(value) and
                    issubclass(value, RefreshableDataView)):
                self.is_refreshable = True
            else:
                value = json.dumps(value)
                self.is_refreshable = False
        self.value = value
        self.display = display
        self.template = template
        self.classes = classes
