import xml.dom.minidom
import xml.etree.ElementTree as ET

class BaseRequest:
    def __init__(self, data):
        self.data = data

    def get(self, name, default = None):
        if name in self.data:
            return self.data[name]
        if name in self.defaults:
            return self.defaults[name]
        return default

    def sub(self, parent, tag, attrs = {}, text = None):
        res = ET.SubElement(parent, tag, attrs)
        if text is not None:
            res.text = str(text)
        return res

    @staticmethod
    def build(name, data):
        type = globals()[name]
        return type(data)

    @staticmethod
    def buildFromArgs(args):
        request = Request.build(args.get('command'), args)
        extensions = args.get('extensions') or []
        if extensions == [] and 'extension' in args:
            extensions = [args.get('extension')]
        for ext in extensions:
            Request.build(ext, args).extend(request)
        return request

    @staticmethod
    def prettifyxml(str):
        dom = xml.dom.minidom.parseString(str)
        return dom.toprettyxml(indent='    ')

class greeting(BaseRequest):
    def __str__(self):
        return 'greeting'

class Request(BaseRequest):
    xmlns = 'urn:ietf:params:xml:ns:epp-1.0'

    def __init__(self, data, object, op):
        self.data       = data
        self.object     = object
        self.op         = op
        self.epp        = ET.Element('epp', {'xmlns': self.xmlns})
        self.command    = None
        self.extension  = None
        if op != 'hello':
            self.command = self.sub(self.epp, 'command')

    def __str__(self, encoding='UTF-8', method='xml'):
        cltrid = self.get('cltrid', (self.object[0] + self.op[0]).upper() + '-0001')
        if cltrid != 'NONE' and self.command is not None:
            self.sub(self.command, 'clTRID', {}, cltrid)
        return ET.tostring(self.epp, encoding, method)

class Extension(BaseRequest):
    def begin(self, request):
        if (request.extension is None):
            request.extension = self.sub(request.command, 'extension')

class FeeCheck(Extension):
    def extend(self, request):
        self.begin(request)
        self.fee = self.sub(request.extension, 'fee:check', {'xmlns:fee': 'urn:ietf:params:xml:ns:fee-0.6'})
        for name in self.get('names').values():
            self.domain = self.sub(self.fee, 'fee:domain')
            self.sub(self.domain, 'fee:name', {}, name)
            self.sub(self.domain, 'fee:command', {}, 'create')
            self.sub(self.domain, 'fee:period', {'unit': 'y'}, '1')

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
        Request.__init__(self, data, 'general', 'login')
        self.login  = self.sub(self.command, 'login')
        self.clid   = self.sub(self.login, 'clID', {}, self.get('login'))
        self.pw     = self.sub(self.login, 'pw', {}, self.get('password'))
        if ('newPassword' in data and data['newPassword']):
            self.sub(self.login, 'newPW', {}, self.get('newPassword'))
        self.ops    = self.sub(self.login, 'options')
        self.ver    = self.sub(self.ops, 'version', {}, self.get('version'))
        self.lang   = self.sub(self.ops, 'lang', {}, self.get('lang'))
        self.svcs   = self.sub(self.login, 'svcs')
        for svc in self.get('svcs'):
            self.sub(self.svcs, 'objURI', {}, svc)

class Hello(Request):
    defaults = {
    }

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

