# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import inspect
import json

from suit_dashboard.views import RefreshableDataView


class Box(object):
    def __init__(self, html_id=None, title=None, description=None,
                 items=None, template=None, context=None,
                 lazy=False, persistent=False, **kwargs):
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
