import xml.dom.minidom
import xml.etree.ElementTree as ET

def build(name, data):
    type = globals()[name]
    return type(data)

class Request:
    xmlns = 'urn:ietf:params:xml:ns:epp-1.0'

    def __init__(self, data):
        self.data       = data
        self.epp        = ET.Element('epp', {'xmlns': self.xmlns})
        self.command    = self.sub(self.epp, 'command')

    def sub(self, parent, tag, attrs = {}, text = None):
        res = ET.SubElement(parent, tag, attrs)
        if text is not None:
            res.text = text
        return res

    def tostring(self, encoding='UTF-8', method='xml'):
        self.sub(self.command, 'clTRID', {}, self.get('cltrid'))
        return ET.tostring(self.epp, encoding, method)

    def toprettyxml(self):
        str = self.tostring()
        dom = xml.dom.minidom.parseString(str)
        return dom.toprettyxml(indent='    ')

    def get(self, name, default = None):
        if name in self.data:
            return self.data[name]
        if name in self.defaults:
            return self.defaults[name]
        return default

class Login(Request):
    defaults = {
        'version': '1.0',
        'lang': 'en',
        'svcs': [
            'urn:ietf:params:xml:ns:host-1.0',
            'urn:ietf:params:xml:ns:domain-1.0',
            'urn:ietf:params:xml:ns:contact-1.0',
        ],
    }

    def __init__(self, data):
        Request.__init__(self, data)
        self.login  = self.sub(self.command, 'login')
        self.clid   = self.sub(self.login, 'clID', {}, self.get('login'))
        self.pw     = self.sub(self.login, 'pw', {}, self.get('password'))
        self.ops    = self.sub(self.login, 'options')
        self.ver    = self.sub(self.ops, 'version', {}, self.get('version'))
        self.lang   = self.sub(self.ops, 'lang', {}, self.get('lang'))
        self.svcs   = self.sub(self.login, 'svcs')
        for svc in self.get('svcs'):
            self.sub(self.svcs, 'objURI', {}, svc)

class Domain(Request):
    defaults = {
        'xmlns:domain': 'urn:ietf:params:xml:ns:domain-1.0'
    }

    def __init__(self, data, op):
        Request.__init__(self, data)
        self.commandOp = self.sub(self.command, op)
        self.domainCommand = self.sub(self.commandOp, 'domain:' + op, {'xmlns:domain': self.get('xmlns:domain')})
class DomainCheck(Domain):
    def __init__(self, data):
        Domain.__init__(self, data, 'check')
        for name in self.get('names').values():
            self.sub(self.domainCommand, 'domain:name', {}, name)

class DomainCreate(Domain):
    def __init__(self, data):
        Domain.__init__(self, data, 'create')
        self.sub(self.domainCommand, 'domain:name', {}, self.get('name'))
        self.sub(self.domainCommand, 'domain:period', {'unit': 'y'}, self.get('period', 1))

