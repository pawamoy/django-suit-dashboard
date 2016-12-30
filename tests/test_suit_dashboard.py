# -*- coding: utf-8 -*-

"""Main test script."""


from django.test import TestCase

import pytest


from suit_dashboard.box import Box, Item
# from suit_dashboard.decorators import refreshable
from suit_dashboard.layout import Column, Grid, Row
# from suit_dashboard.urls import get_refreshable_urls
from suit_dashboard.views import DashboardView  # , RefreshableDataView


class MainTestCase(TestCase):
    """Main Django test case."""

    def test_main(self):
        """Main test method."""
        box = Box(items=[Item()])
        grid = Grid(Row(Column(width=12)))
        view = DashboardView()

        assert box
        assert grid
        assert view


class BoxTestCase(TestCase):
    """Box test case."""

    def test_box_items_type(self):
        """Test raising of errors when items type are wrong."""
        with pytest.raises(AttributeError) as e:
            Box(items=1)
        assert 'Box items attribute must be a list or tuple' in str(e.value)

        with pytest.raises(ValueError) as e:
            Box(items=[Item(), 0])
        assert 'All elements of Box must be Item instances' in str(e.value)

    def test_box_kwargs(self):
        """Test box correctly setting up kwargs as attributes."""
        box = Box(arg1=1, arg2=2, arg3=3)
        assert hasattr(box, 'arg1')
        assert getattr(box, 'arg1') == 1
        assert hasattr(box, 'arg2')
        assert getattr(box, 'arg2') == 2
        assert hasattr(box, 'arg3')
        assert getattr(box, 'arg3') == 3


class ItemTestCase(TestCase):
    """Item test case."""


class GridTestCase(TestCase):
    """Grid test case."""

    def test_grid_columns_type(self):
        """Test raising of errors when items type are wrong."""
        with pytest.raises(TypeError) as e:
            Grid(1)
        assert 'All elements of Grid must be Row instances' in str(e.value)


class RowTestCase(TestCase):
    """Row test case."""

    def test_row_columns_type(self):
        """Test raising of errors when items type are wrong."""
        with pytest.raises(TypeError) as e:
            Row(1)
        assert 'All elements of Row must be Column instances' in str(e.value)


class ColumnTestCase(TestCase):
    """Column test case."""

    def test_column_columns_type(self):
        """Test raising of errors when items type are wrong."""
        with pytest.raises(TypeError) as e:
            Column(1)
        assert 'All elements of Column must be Row or Box instances' in str(e.value)  # noqa
        with pytest.raises(ValueError) as e:
            Column(width=15)
        assert 'Column width must be between 1 and 12' in str(e.value)
