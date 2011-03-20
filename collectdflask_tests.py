#!/usr/bin/env python
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import collectdflask
from lxml import etree
import os

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
collectdflask.app.config['COLLECTD_DATA_DIR'] = TEST_DATA_DIR

class TestDataDirParsing(unittest.TestCase):

    def setUp(self):
        self.app = collectdflask.app.test_client()

    def test_get_hosts(self):
        hosts = collectdflask.get_hosts()
        self.assertEqual(
            hosts,
	    ['host1', 'host2', 'host3'],
        )

    def test_get_hosts_wildcard(self):
        hosts = collectdflask.get_hosts('*')
        self.assertEqual(
            hosts,
	    ['host1', 'host2', 'host3'],
        )

    def test_get_host_pattern(self):
        hosts = collectdflask.get_hosts('*1')
        self.assertEqual(
            hosts,
	    ['host1'],
        )

    def test_get_plugins_for_host(self):
        plugins = collectdflask.get_plugins_for_host('host1')
        self.assertEqual(
            plugins,
            ['plugin1'],
        )

    def test_get_plugins_for_host_pattern(self):
        plugins = collectdflask.get_plugins_for_host('host3', '*3')
        self.assertEqual(
            plugins,
            ['plugin3'],
        )

    def test_get_plugins_for_host_wildcard(self):
        plugins = collectdflask.get_plugins_for_host('host3', '*')
        self.assertEqual(
            plugins,
            ['plugin1', 'plugin2', 'plugin3'],
        )


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = collectdflask.app.test_client()

    def test_index(self):
        response = self.app.get('/')
        tree = etree.fromstring(response.data)
        ul = tree.findall('.//ul/li')
        result = {}
        for entry in ul:
            links = entry.findall('.//a')
            result[links[0].text] = [a.text for a in links[1:]]
        self.assertEqual(
            result,
            {
               'host1' : ['plugin1'],
	       'host2' : ['plugin1', 'plugin2'],
	       'host3' : ['plugin1', 'plugin2', 'plugin3'],
            },
        )


if __name__ == '__main__':
    unittest.main()
