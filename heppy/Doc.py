# -*- coding: utf-8 -*-

from importlib import import_module


class Doc:
    nsmap = {
        'builtin':      'builtin',
        'epp':          'urn:ietf:params:xml:ns:epp-1.0',
        'host':         'urn:ietf:params:xml:ns:host-1.0',
        'domain':       'urn:ietf:params:xml:ns:domain-1.0',
        'contact':      'urn:ietf:params:xml:ns:contact-1.0',
        'secDNS':       'urn:ietf:params:xml:ns:secDNS-1.1',
        'launch':       'urn:ietf:params:xml:ns:launch-1.0',
        'fee':          'urn:ietf:params:xml:ns:fee-0.7',
        'fee05':        'urn:ietf:params:xml:ns:fee-0.5',
        'fee06':        'urn:ietf:params:xml:ns:fee-0.6',
        'fee07':        'urn:ietf:params:xml:ns:fee-0.7',
        'fee08':        'urn:ietf:params:xml:ns:fee-0.8',
        'fee09':        'urn:ietf:params:xml:ns:fee-0.9',
        'fee10':        'urn:ietf:params:xml:ns:epp:fee-1.0',
        'fee11':        'urn:ietf:params:xml:ns:fee-0.11',
        'fee21':        'urn:ietf:params:xml:ns:fee-0.21',
        'fee23':        'urn:ietf:params:xml:ns:fee-0.23',
        'rgp':          'urn:ietf:params:xml:ns:rgp-1.0',
        'smd':          'urn:ietf:params:xml:ns:signedMark-1.0',
        'mark':         'urn:ietf:params:xml:ns:mark-1.0',
        'oxrs':         'urn:afilias:params:xml:ns:oxrs-1.1',
        'namestoreExt': 'http://www.verisign-grs.com/epp/namestoreExt-1.1',
        'idn':          'urn:afilias:params:xml:ns:idn-1.0',
        'idnLang':      'http://www.verisign.com/epp/idnLang-1.0',
        'price':        'urn:ar:params:xml:ns:price-1.1',
        'price10':      'urn:ar:params:xml:ns:price-1.0',
        'price11':      'urn:ar:params:xml:ns:price-1.1',
        'price12':      'urn:ar:params:xml:ns:price-1.2',
        'domain_hm':    'http://hostmaster.ua/epp/domain-1.1',
        'host_hm':      'http://hostmaster.ua/epp/host-1.1',
        'contact_hm':   'http://hostmaster.ua/epp/contact-1.1',
        'rgp_hm':       'http://hostmaster.ua/epp/rgp-1.1',
        'secDNShm':     'http://hostmaster.ua/epp/secDNS-1.1',
        'uaepp':        'http://hostmaster.ua/epp/uaepp-1.1',
        'balance':      'http://hostmaster.ua/epp/balance-1.0',
        'keysys':       'http://www.key-systems.net/epp/keysys-1.0',
        'charge':       'http://www.unitedtld.com/epp/charge-1.0',
        'finance':      'http://www.unitedtld.com/epp/finance-1.0',
        'association':  'urn:afilias:params:xml:ns:association-1.0',
        'urc':          'http://ns.uniregistry.net/centric-1.0',
        'sync':         'http://www.verisign.com/epp/sync-1.0',
        'neulevel':     'urn:ietf:params:xml:ns:neulevel',
        'neulevel10':   'urn:ietf:params:xml:ns:neulevel-1.0',
        'kv':           'urn:X-ar:params:xml:ns:kv-1.0',
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
        if not self.modules:
            for name, nsi in self.nsmap.items():
                self.modules[nsi] = name
        module = self.modules.get(ns)
        if isinstance(module, bytes):
            module = module.decode('utf-8')
        if isinstance(module, str):
            module = self.build_module(ns, module)
            self.modules[ns] = module
        return module

    def build_module(self, ns, name):
        lib = import_module('heppy.modules.' + name)
        klass = getattr(lib, name)
        return klass(ns)

    def get(self, name, default=None):
        return self.data.get(name, default)

    def has(self, name):
        return name in self.data

    @staticmethod
    def mget(data, map):
        return {k: data.get(v or k) for k, v in map.items()}

    def set(self, name, value):
        self.data[name] = value

