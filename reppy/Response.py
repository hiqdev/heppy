import xml.etree.ElementTree as ET
from importlib import import_module

from pprint import pprint

from Worker import Worker

class Response(Worker):
    def __init__(self, root):
        self.data = {}
        self.root = root
        self.parse(self.root[0])

    def find(self, tag, name):
        return tag.find(name, namespaces=self.nsmap)

    def findall(self, tag, name):
        return tag.findall(name, self.nsmap)

    def parse(self, tag):
        ns = tag.tag.split('}')[0][1:]
        name = tag.tag.split('}')[1]
        module = self.get_module(ns)
        if name in module.opmap:
            name = module.opmap[name]
        method = 'parse_' + name
        if not hasattr(module, method):
            raise Exception('unknown tag', ns + ':' + name)
        getattr(module, method)(self, tag)

    @staticmethod
    def parsexml(xml):
        root = ET.fromstring(xml)
        return Response(root)

    @staticmethod
    def build(name, start):
        type = globals()[name]
        return type(start)

