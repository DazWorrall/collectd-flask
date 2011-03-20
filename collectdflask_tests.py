#!/usr/bin/env python
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import collectdflask
import os

class TestCollectdFlask(unittest.TestCase):

    def setUp(self):
        self.app = collectdflask.app.test_client()


if __name__ == '__main__':
    unittest.main()
