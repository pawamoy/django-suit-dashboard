# -*- coding: utf-8 -*-

"""
Layout module.

This module provides three classes: Grid, the root of the layout which contains
instances of Row, the class to build a new row, which in their turn contain
instances of Column, the class to build a new column. You nest new rows into
columns. A column also contain boxes.
"""

from __future__ import unicode_literals
from suit_dashboard.box import Box


class Grid(object):
    """Grid class. Root of the layout. Contains rows."""

    def __init__(self, *rows, **kwargs):
        """
        Init method.

        Args:
            *rows (): the instances of Row.
            **kwargs (): not used.
        """
        if not all([isinstance(r, Row) for r in rows]):
            raise TypeError('All elements of Grid must be Row instances')
        self.type = 'grid'
        self.rows = rows


class Row(object):
    """Row class. Contains columns."""

    def __init__(self, *columns, **kwargs):
        """
        Init method.

        Args:
            *columns (): the instances of Column.
            **kwargs (): not used.
        """
        if not all([isinstance(c, Column) for c in columns]):
            raise TypeError('All elements of Row must be Column instances')
        self.type = 'row'
        self.columns = columns


class Column(object):
    """Column class. Contains rows and/or boxes."""

    def __init__(self, *elements, **kwargs):
        """
        Init method.

        Args:
            *elements (): the rows or boxes.
            **kwargs: the width can be passed through the keyword args [1-12].
        """
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
