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
        'fee05':        'urn:ietf:params:xml:ns:fee-0.5',
        'fee06':        'urn:ietf:params:xml:ns:fee-0.6',
        'fee07':        'urn:ietf:params:xml:ns:fee-0.7',
        'fee08':        'urn:ietf:params:xml:ns:fee-0.8',
        'fee09':        'urn:ietf:params:xml:ns:fee-0.9',
        'fee11':        'urn:ietf:params:xml:ns:fee-0.11',
        'fee21':        'urn:ietf:params:xml:ns:fee-0.21',
        'rgp':          'urn:ietf:params:xml:ns:rgp-1.0',
        'oxrs':         'urn:afilias:params:xml:ns:oxrs-1.1',
        'namestoreExt': 'http://www.verisign-grs.com/epp/namestoreExt-1.1',
        'idn':          'urn:afilias:params:xml:ns:idn-1.0',
        'idnLang':      'http://www.verisign.com/epp/idnLang-1.0',
        'price':        'urn:ar:params:xml:ns:price-1.1'
    }

    okcodes = {
        '1000': 'completed',
        '1001': 'pending',
        '1300': 'no messages',
        '1301': 'ack to dequeue',
        '1500': 'ending session',
    }

    modules = {}

    def get_module(self, ns):
        if ns in self.nsmap:
            ns = self.nsmap[ns]
        if self.modules == {}:
            for name, nsi in self.nsmap.iteritems():
                self.modules[nsi] = name
        module = self.modules.get(ns)
        if isinstance(module, basestring):
            module = self.build_module(ns, module)
            self.modules[ns] = module
        return module

    def build_module(self, ns, name):
        lib = import_module('heppy.modules.' + name)
        type = getattr(lib, name)
        return type(ns)

    def get(self, name, default=None):
        return self.data.get(name, default)

    def has(self, name):
        return name in self.data

    @staticmethod
    def mget(data, map):
        return {k: data.get(v or k) for k, v in map.iteritems()}

    def set(self, name, value):
        self.data[name] = value
