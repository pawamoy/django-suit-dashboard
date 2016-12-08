# -*- coding: utf-8 -*-

"""Main test script."""



from django.test import TestCase

import suit_dashboard


class MainTestCase(TestCase):
    """Main Django test case"""
    def setUp(self):
        pass

    def test_main(self):
        assert suit_dashboard

    def tearDown(self):
        pass
