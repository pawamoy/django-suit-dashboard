# -*- coding: utf-8 -*-

"""
Layout module.

This module provides three classes: Grid, the root of the layout which contains
instances of Row, the class to build a new row, which in their turn contain
instances of Column, the class to build a new column. You nest new rows into
columns. A column also contain boxes.
"""

from __future__ import unicode_literals

from .widgets import Widget


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


class Box(object):
    """
    Box class.

    A box can be built directly passing values to the constructor. Another way
    you can use it is to create a subclass, and writing a getter for each
    wanted attribute. It will allow the box to be loaded lazily, but also to
    store the values returned by getters in private attributes that can be
    reused later without computing them again.
    """

    def __init__(self,
                 html_id=None,
                 title=None,
                 description=None,
                 widgets=None,
                 template=None,
                 context=None,
                 **kwargs):
        """
        Init method.

        Args:
            html_id (str): an ID to set on the HTML box.
            title (str): a title to display on the top of the box.
            description (str): a description to display after the title box.
            widgets (list): the box's list of widgets.
            template (str): the path to a custom template to use for this box.
            context (dict): additional context to pass to the box.
        """
        if widgets is not None:
            if not isinstance(widgets, (list, tuple)):
                raise AttributeError('Box widgets attribute '
                                     'must be a list or tuple')
            if not all([isinstance(e, Widget) for e in widgets]):
                raise ValueError('All elements of Box must be Widget instances')  # noqa

            try:
                self.widgets = widgets
            except AttributeError:
                self._widgets = widgets

        self.type = 'box'

        if html_id is not None:
            try:
                self.html_id = html_id
            except AttributeError:
                self._html_id = html_id
        if title is not None:
            try:
                self.title = title
            except AttributeError:
                self._title = title
        if description is not None:
            try:
                self.description = description
            except AttributeError:
                self._description = description
        if template is not None:
            try:
                self.template = template
            except AttributeError:
                self._template = template
        if context is not None:
            try:
                self.context = context
            except AttributeError:
                self._context = context

        for kw, arg in kwargs.items():
            setattr(self, kw, arg)
