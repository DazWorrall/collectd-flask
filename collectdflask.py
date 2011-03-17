#!/usr/bin/python
from flask import Flask, render_template, request
from json import loads
from httplib2 import Http
import sys
import fnmatch

COLLECTD_WEB_URL = 'http://example.com/cgi-bin'
COLLECTD_WEB_PREFIX = 'http://example.com'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('CF_SETTINGS', silent=True)

h = Http()

cache = {}

def json_request(action, **parameters):
    key = repr((action, parameters))
    if cache.has_key(key):
        return cache[key]
    uri = ['%s/cgi-bin/collection.modified.cgi?action=%s' % (app.config['COLLECTD_WEB_URL'], action)]
    uri = uri + ['%s=%s' % (k, v) for k, v in parameters.items()]
    res, body = h.request(';'.join(uri))
    decoded_object = loads(body)
    cache[key] = decoded_object
    if app.debug:
        print >>sys.stderr, key
    return decoded_object

def get_hosts():
    return json_request('hostlist_json')

def graph(hosts, plugins, period='month'):
    graphs = {}
    for host in hosts:
        graphs[host] = {}
        for plugin in plugins[host]:
            graphs[host][plugin] = [app.config['COLLECTD_WEB_PREFIX'] + x for x in json_request('graphs_json', host=host, plugin=plugin)[period]]
    return render_template('graph.html', hosts=hosts, plugins=plugins, graphs=graphs, period=period)

@app.route('/')
def index():
    period = request.args.get('period', 'month')
    hosts = get_hosts()
    plugins = {}
    for host in hosts:
        plugins[host] = json_request('pluginlist_json', host=host)
    return render_template('index.html', hosts=hosts, plugins=plugins, period=period)

@app.route('/<hostname>/')
def graph_by_host(hostname):
    hosts = [h for h in get_hosts() if fnmatch.fnmatch(h, hostname)]
    plugins = {}
    for h in hosts:
        plugins[h] =  json_request('pluginlist_json', host=h)
    return graph(hosts, plugins, request.args.get('period', 'month'))

@app.route('/<hostname>/<plugin>/')
def graph_by_host_with_plugin(hostname, plugin):
    hosts = [hostname]
    plugins = {hostname: [plugin]}
    return graph(hosts, plugins, request.args.get('period', 'month'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
