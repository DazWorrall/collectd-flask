#!/usr/bin/env python
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import collectdflask
import os

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
collectdflask.app.config['COLLECTD_DATA_DIR'] = TEST_DATA_DIR

class TestCollectdFlask(unittest.TestCase):

    def setUp(self):
        self.app = collectdflask.app.test_client()

    def test_get_hosts(self):
        hosts = collectdflask.get_hosts()
        self.assertEqual(
            sorted(hosts),
	    ['host1', 'host2', 'host3'],
        )

    def test_get_hosts_wildcard(self):
        hosts = collectdflask.get_hosts('*')
        self.assertEqual(
            sorted(hosts),
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
            sorted(plugins),
            ['plugin1', 'plugin2', 'plugin3'],
        )


if __name__ == '__main__':
    unittest.main()
