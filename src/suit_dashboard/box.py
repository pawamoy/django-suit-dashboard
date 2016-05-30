# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Box(object):
    def __init__(self, html_id=None, title=None, description=None,
                 items=None, template=None, **context):
        if items:
            if not (isinstance(items, list) or isinstance(items, tuple)):
                raise AttributeError('Box items attribute '
                                     'must be a list or tuple')
            if not all([isinstance(e, Item) for e in items]):
                raise ValueError('All elements of Box must be Item instances')
            self._items = items

        if html_id:
            self._html_id = html_id
        if title:
            self._title = title
        if description:
            self._description = description
        if template:
            self._template = template
        if context:
            self._context = context

        self.type = 'box'

    @property
    def html_id(self):
        if not hasattr(self, '_html_id'):
            self._html_id = self.get_html_id()
        return self._html_id

    def get_html_id(self):
        return ''

    @property
    def title(self):
        if not hasattr(self, '_title'):
            self._title = self.get_title()
        return self._title

    def get_title(self):
        return ''

    @property
    def description(self):
        if not hasattr(self, '_description'):
            self._description = self.get_description()
        return self._description

    def get_description(self):
        return ''

    @property
    def template(self):
        if not hasattr(self, '_template'):
            self._template = self.get_template()
        return self._template

    def get_template(self):
        return ''

    @property
    def items(self):
        if not hasattr(self, '_items'):
            self._items = self.get_items()
        return self._items

    def get_items(self):
        return []

    @property
    def context(self):
        if not hasattr(self, '_context'):
            self._context = self.get_context()
        return self._context

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
        self.value = value
        self.display = display
        self.template = template
        self.classes = classes
