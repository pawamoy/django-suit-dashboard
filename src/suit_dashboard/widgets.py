# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Widget(object):
    def __init__(self, id=None, title=None, description=None,
                 context=None, template=None):
        if context:
            if not (isinstance(context, list) or isinstance(context, tuple)):
                raise AttributeError('Widget context attribute '
                                     'must be a list or tuple')
            if not all([(isinstance(e, WidgetGroup) or
                         isinstance(e, WidgetItem)) for e in Widget]):
                raise ValueError('Elements of Widget context must be '
                                 'WidgetGroup or WidgetItem instances')
            self.context = context

        if id:
            self.id = id
        if title:
            self.title = title
        if description:
            self.description = description
        if template:
            self.template = template

        self.type = 'widget'


class WidgetGroup(object):
    AS_TABLE = 'table'
    AS_LIST = 'list'

    def __init__(self, id, name, items, display='table', classes=''):
        self.type = 'group'
        self.id = id
        self.name = name
        self.display = display
        self.items = items
        self.classes = classes


class WidgetItem(object):
    def __init__(self, id, name, value, is_chart=False):
        self.type = 'item'
        self.id = id
        self.name = name
        self.value = value
        self.is_chart = is_chart
