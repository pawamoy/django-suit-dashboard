# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import inspect

from suit_dashboard.views import RefreshableDataView


class Box(object):
    def __init__(self, html_id=None, title=None, description=None,
                 items=None, template=None, context=None, **kwargs):
        if items:
            if not (isinstance(items, list) or isinstance(items, tuple)):
                raise AttributeError('Box items attribute '
                                     'must be a list or tuple')
            if not all([isinstance(e, Item) for e in items]):
                raise ValueError('All elements of Box must be Item instances')
            self._items = items

        if html_id:
            self.html_id = html_id
        else:
            self.html_id = self.get_html_id()
        if title:
            self.title = title
        else:
            self.title = self.get_title()
        if description:
            self.description = description
        else:
            self.description = self.get_description()
        if template:
            self.template = template
        else:
            self.template = self.get_template()
        if items:
            self.items = items
        else:
            self.items = self.get_items()
        if context:
            self.context = context
        else:
            self.context = self.get_context()
        if kwargs:
            self.kwargs = kwargs

        self.type = 'box'

    def get_html_id(self):
        return ''

    def get_title(self):
        return ''

    def get_description(self):
        return ''

    def get_template(self):
        return ''

    def get_items(self):
        return []

    def get_context(self):
        return {}


class Item(object):
    AS_TABLE = 'table'
    AS_LIST = 'list'
    AS_HIGHCHARTS = 'highcharts'

    def __init__(self, html_id=None, name=None, value=None,
                 display=None, template=None, classes=''):
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
