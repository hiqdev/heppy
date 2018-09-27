from collections import OrderedDict

from ..Module import Module

class domain(Module):
    opmap = {
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'ns':           'descend',
        'authInfo':     'descend',
        'name':         'set',
        'roid':         'set',
        'clID':         'set',
        'crID':         'set',
        'upID':         'set',
        'crDate':       'set',
        'upDate':       'set',
        'exDate':       'set',
        'trDate':       'set',
        'pw':           'set',
        'registrant':   'set',
    }

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

    def parse_hostObj(self, response, tag):
        response.addpair('nss', tag.text.lower())

    def parse_host(self, response, tag):
        response.addpair('hosts', tag.text.lower())

    def parse_contact(self, response, tag):
        response.set(tag.attrib['type'], tag.text)

### REQUEST rendering

    def render_check(self, request):
        command = self.render_command(request, 'check')
        for name in request.get('names').itervalues():
            request.sub(command, 'domain:name', {}, name)

    def render_info(self, request):
        hosts = request.get('hosts', 'all')
        command = self.render_command_fields(request, 'info', {'name': {'hosts': hosts}})
        if request.has('pw'):
            self.render_auth_info(request, command)

    def render_auth_info(self, request, command, pw=None, attrs={}):
        if pw is None:
            pw = request.get('pw', '')
        authInfo = request.sub(command, 'domain:authInfo')
        request.sub(authInfo, 'domain:pw', attrs, pw)

    def render_transfer(self, request):
        attrs = {'op': request.get('op') or 'request'}
        command = self.render_command_fields(request, 'transfer', OrderedDict([
            ('name', {}),
            ('period', {'unit': 'y'}),
        ]), attrs)
        if request.has('pw') or attrs.get('op') == 'request':
            roid = {'roid': request.get('roid')} if request.has('roid') else {}
            self.render_auth_info(request, command, attrs=roid)

    def render_create(self, request):
        command = self.render_command_fields(request, 'create', OrderedDict([
            ('name', {}),
            ('period', {'unit': 'y'}),
            ('registrant', {}),
        ]))

        if request.get('ns'):
            ns = request.sub(command, 'domain:ns')
            for host in request.get('ns').itervalues():
                request.sub(ns, 'domain:hostObj', text=host)

        for contactType in ('admin', 'tech', 'billing'):
            if request.has(contactType):
                request.sub(command, 'domain:contact', {'type': contactType}, request.get(contactType))
        self.render_auth_info(request, command)

    def render_delete(self, request):
        self.render_command_fields(request, 'delete')

    def render_renew(self, request):
        self.render_command_fields(request, 'renew', OrderedDict([
            ('name', {}),
            ('curExpDate', {}),
            ('period', {'unit': 'y'}),
        ]))

    def render_update(self, request):
        command = self.render_command_fields(request, 'update')
