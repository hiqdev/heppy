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

    CONTACT_TYPES = (
        'admin',
        'tech',
        'billing'
    )

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

        if request.has('nss'):
            self.render_nss(request, command, request.get('nss'))
        if self.has_contacts(request.data):
            self.render_contacts(request, command)
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

        if request.has('add'):
            self.render_update_section(request, command, 'add')

        if request.has('rem'):
            self.render_update_section(request, command, 'rem')

        if request.has('chg'):
            chgElement = request.sub(command, 'domain:chg')
            chgData = request.data['chg']
            request.sub(chgElement, 'domain:registrant', text=chgData['registrant'])
            self.render_auth_info(request, chgElement, chgData.get('pw'))

    def render_update_section(self, request, command, operation):
        element = request.sub(command, 'domain:' + operation)
        data = request.data.get(operation)
        if 'nss' in data:
            self.render_nss(request, element, data['nss'])
        if self.has_contacts(data):
            self.render_contacts(request, element, data)
        if 'statuses' in data:
            self.render_statuses(request, element, data['statuses'])

    def render_auth_info(self, request, parent, pw=None, attrs={}):
        if pw is None:
            pw = request.get('pw', '')
        authInfo = request.sub(parent, 'domain:authInfo')
        request.sub(authInfo, 'domain:pw', attrs, pw)

    def render_nss(self, request, parent, hosts):
        nsElement = request.sub(parent, 'domain:ns')
        for host in hosts.itervalues():
            request.sub(nsElement, 'domain:hostObj', text=host)

    def render_contacts(self, request, parent, storage=None):
        storage = storage or request.data
        for contactType in set(self.CONTACT_TYPES) & set(storage.keys()):
            request.sub(parent, 'domain:contact', {'type': contactType}, storage[contactType])

    def render_statuses(self, request, parent, statusData):
        for status, description in statusData.iteritems():
            request.sub(parent, 'domain:status', {'s': status}, description)

    def has_contacts(self, storage):
        return any(contactType in storage for contactType in self.CONTACT_TYPES)
