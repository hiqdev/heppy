from importlib import import_module

class Doc:
    nsmap = {
        'builtin':      'builtin',
        'epp':          'urn:ietf:params:xml:ns:epp-1.0',
        'host':         'urn:ietf:params:xml:ns:host-1.0',
        'domain':       'urn:ietf:params:xml:ns:domain-1.0',
        'contact':      'urn:ietf:params:xml:ns:contact-1.0',
        'secDNS':       'urn:ietf:params:xml:ns:secDNS-1.1',
        'fee':          'urn:ietf:params:xml:ns:fee-0.7',
        'rgp':          'urn:ietf:params:xml:ns:rgp-1.0',
        'oxrs':         'urn:afilias:params:xml:ns:oxrs-1.1',
        'namestoreExt': 'http://www.verisign-grs.com/epp/namestoreExt-1.1',
    }

    okcodes = {
        '1000': 'completed',
        '1001': 'pending',
        '1300': 'no messages',
        '1301': 'ack to dequeue',
        '1500': 'ending session',
    }

    modules = {}

    def __init__(self, root):
        for name,ns in self.nsmap.iteritems():
            self.modules[ns] = name

    def get_module(self, ns):
        if ns in self.nsmap:
            ns = self.nsmap[ns]
        module = self.modules[ns]
        if isinstance(module, basestring):
            module = self.build_module(ns, module)
            self.modules[ns] = module
        return module

    def build_module(self, ns, name):
        lib = import_module('heppy.modules.' + name)
        type = getattr(lib, name)
        return type(ns)

    def get(self, name, default = None):
        return self.data.get(name, default)

    @staticmethod
    def mget(data, map):
        return {k:data.get(v or k) for k,v in map.iteritems()}

    def set(self, name, value):
        self.data[name] = value

    def addto(self, name, values):
        if not name in self.data:
            self.data[name] = {}
        for k,v in values.iteritems():
            self.data[name][k] = v

    def addpair(self, name, value):
        self.addto(name, {value: value})

