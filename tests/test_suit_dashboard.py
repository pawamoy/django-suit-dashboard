# -*- coding: utf-8 -*-

"""Main test script."""


from django.test import TestCase

import suit_dashboard


class MainTestCase(TestCase):
    """Main Django test case."""

    def setUp(self):
        """Setup method."""
        self.package = suit_dashboard

    def test_main(self):
        """Main test method."""
        assert self.package

    def tearDown(self):
        """Tear down method."""
        del self.package
