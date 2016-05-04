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
        else:
            self.context = self.get_context()

        if id:
            self.id = id
        else:
            self.id = self.get_id()
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

        self.type = 'widget'

    def get_id(self):
        return ''

    def get_title(self):
        return ''

    def get_description(self):
        return ''

    def get_template(self):
        return ''

    def get_context(self):
        return []


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
    def __init__(self, id, name, value, is_chart=False, classes=''):
        self.type = 'item'
        self.id = id
        self.name = name
        if not (isinstance(value, list) or isinstance(value, tuple)):
            self.value = (value, )
        else:
            self.value = value
        self.is_chart = is_chart
        self.classes = classes

