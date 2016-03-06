import xml.etree.ElementTree as ET
from importlib import import_module

from pprint import pprint

class Response:
    nsmap = {
        'epp':          'urn:ietf:params:xml:ns:epp-1.0',
        'domain':       'urn:ietf:params:xml:ns:domain-1.0',
        'oxrs':         'urn:afilias:params:xml:ns:oxrs-1.1',
        'fee':          'urn:ietf:params:xml:ns:fee-0.7',
        'namestore':    'http://www.verisign-grs.com/epp/namestoreExt-1.1',
    }

    okcodes = {
        '1000': 'completed',
        '1001': 'pending',
        '1300': 'no messages',
        '1301': 'ack to dequeue',
        '1500': 'ending session',
    }

    @staticmethod
    def parsexml(xml):
        root = ET.fromstring(xml)
        return Response(root)

    @staticmethod
    def build(name, start):
        type = globals()[name]
        return type(start)

    def find(self, tag, name):
        return tag.find(name, namespaces=self.nsmap)

    def findall(self, tag, name):
        return tag.findall(name, self.nsmap)

    def __init__(self, root):
        self.data = {}
        self.root = root
        self.modules = {}
        for name,ns in self.nsmap.iteritems():
            self.modules[ns] = name
        self.parse(self.root[0])

    def get_module(self, ns):
        module = self.modules[ns]
        if isinstance(module, basestring):
            lib = import_module('reppy.' + module)
            type = getattr(lib, module)
            module = type(self)
            self.modules[ns] = module
        return module

    def parse(self, tag):
        ns = tag.tag.split('}')[0][1:]
        name = tag.tag.split('}')[1]
        module = self.get_module(ns)
        if name in module.opmap:
            name = module.opmap[name]
        method = 'parse_' + name
        if not hasattr(module, method):
            raise Exception('unknown tag', ns + ':' + name)
        getattr(module, method)(tag)

    def set(self, name, value):
        self.data[name] = value

    def get(self, name, default):
        return self.data.get(name, default)

