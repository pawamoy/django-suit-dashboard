# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Grid(object):
    def __init__(self, rows):
        if not (isinstance(rows, list) or isinstance(rows, tuple)):
            raise TypeError('Grid elements attribute '
                            'must be a list or tuple')
        if not all([isinstance(r, Row) for r in rows]):
            raise TypeError('All elements of Grid '
                            'must be Row instances')
        self.type = 'grid'
        self.rows = rows


class Row(object):
    def __init__(self, columns):
        if not (isinstance(columns, list) or isinstance(columns, tuple)):
            raise TypeError('Row elements attribute '
                            'must be a list or tuple')
        if not all([isinstance(c, Column) for c in columns]):
            raise TypeError('All elements of Row '
                            'must be Column instances')
        self.type = 'row'
        self.columns = columns


class Column(object):
    def __init__(self, elements, width=12):
        if not (isinstance(elements, list) or isinstance(elements, tuple)):
            raise TypeError('Column elements attribute '
                            'must be a list or tuple')
        if any([isinstance(e, Column) for e in elements]):
            raise TypeError('Elements of Column '
                            'cannot be Column instances')
        if width not in range(1, 13):
            raise ValueError('Column width must be between 1 and 12')

        self.type = 'column'
        self.elements = elements
        self.width = width
