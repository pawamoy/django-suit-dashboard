# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from suit_dashboard.box import Box


class Grid(object):
    def __init__(self, *rows, **kwargs):
        if not all([isinstance(r, Row) for r in rows]):
            raise TypeError('All elements of Grid must be Row instances')
        self.type = 'grid'
        self.rows = rows


class Row(object):
    def __init__(self, *columns, **kwargs):
        if not all([isinstance(c, Column) for c in columns]):
            raise TypeError('All elements of Row must be Column instances')
        self.type = 'row'
        self.columns = columns


class Column(object):
    def __init__(self, *elements, **kwargs):
        if not all([isinstance(e, Row) or issubclass(type(e), Box)
                    for e in elements]):
            raise TypeError('All elements of Column must '
                            'be Row or Box instances')
        width = kwargs.pop('width', 12)
        if width not in range(1, 13):
            raise ValueError('Column width must be between 1 and 12')

        self.type = 'column'
        self.elements = elements
        self.width = width
