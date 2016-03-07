import xml.dom.minidom
import xml.etree.ElementTree as ET

from pprint import pprint
from Worker import Worker

class Request(Worker):
    xmlns = 'urn:ietf:params:xml:ns:epp-1.0'

    def __init__(self, data):
        Worker.__init__(self, data)
        self.data       = data
        self.raw        = None
        self.epp        = None
        self.command    = None
        self.extension  = None

    def old_init(self):
        self.epp        = ET.Element('epp', {'xmlns': self.xmlns})
        if op != 'hello':
            self.command = self.sub(self.epp, 'command')

    def __str__(self, encoding='UTF-8', method='xml'):
        if self.raw is None:
            return ET.tostring(self.epp, encoding, method)
        else:
            return self.raw

    def element(self, tag, attrs = {}, text = None):
        res = ET.Element(tag, attrs)
        if text is not None:
            res.text = str(text)
        return res

    def sub(self, parent, tag, attrs = {}, text = None):
        res = ET.SubElement(parent, tag, attrs)
        if text is not None:
            res.text = str(text)
        return res

    def subfields(self, parent, fields):
        name = parent.tag.split(':')[0]
        for field, attrs in fields.iteritems():
            self.sub(parent, name + ':' + field, attrs, self.get(field))
        return parent

    @staticmethod
    def build(command, data, extensions = []):
        request = Request(data)
        request.render(command)
        for ext in extensions:
            request.render(ext)
        request.render('epp:clTRID')
        return request

    @staticmethod
    def buildFromArgs(args):
        extensions = args.get('extensions') or []
        if extensions == [] and 'extension' in args:
            extensions = [args.get('extension')]
        return Request.build(args.get('command'), args, extensions)

    def render(self, command):
        ns = command.split(':')[0]
        name = command.split(':')[1]
        module = self.get_module(ns)
        method = 'render_' + name
        if not hasattr(module, method):
            raise Exception('unknown command', ns + ':' + name)
        getattr(module, method)(self)

    @staticmethod
    def prettifyxml(request):
        string = str(request)
        if string[0] != '<':
            return string
        dom = xml.dom.minidom.parseString(string)
        return dom.toprettyxml(indent='    ')

class Hello(Request):
    def __init__(self, data):
        Request.__init__(self, data, 'general', 'hello')
        self.commandOp = self.sub(self.epp, 'hello')

class Domain(Request):
    defaults = {
        'xmlns:domain': 'urn:ietf:params:xml:ns:domain-1.0'
    }

    def __init__(self, data, op):
        Request.__init__(self, data, 'domain', op)
        self.commandOp = self.sub(self.command, op)
        self.domainCommand = self.sub(self.commandOp, 'domain:' + op, {'xmlns:domain': self.get('xmlns:domain')})

class DomainCheck(Domain):
    def __init__(self, data):
        Domain.__init__(self, data, 'check')
        for name in self.get('names').values():
            self.sub(self.domainCommand, 'domain:name', {}, name)

class DomainInfo(Domain):
    def __init__(self, data):
        Domain.__init__(self, data, 'info')
        self.sub(self.domainCommand, 'domain:name', {'hosts': 'all'}, self.get('name'))

class DomainCreate(Domain):
    def __init__(self, data):
        Domain.__init__(self, data, 'create')
        self.sub(self.domainCommand, 'domain:name', {}, self.get('name'))
        self.sub(self.domainCommand, 'domain:period', {'unit': 'y'}, self.get('period', 1))
        if self.get('registrant'):
            self.sub(self.domainCommand, 'domain:registrant', {}, self.get('registrant'))
        for type in ('admin', 'tech', 'billing'):
            if self.get(type):
                self.sub(self.domainCommand, 'domain:contact', {'type': type}, self.get(type))
        self.authInfo = self.sub(self.domainCommand, 'domain:authInfo')
        self.sub(self.authInfo, 'domain:pw', {}, self.get('password', ''))

class DomainDelete(Domain):
    def __init__(self, data):
        Domain.__init__(self, data, 'delete')
        self.sub(self.domainCommand, 'domain:name', {}, self.get('name'))

