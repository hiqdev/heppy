from collections import OrderedDict
from pprint import pprint

from ..Module import Module
from ..TagData import TagData


class domain(Module):
    opmap = {
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'renData':      'descend',
        'trnData':      'descend',
        'ns':           'descend',
        'authInfo':     'descend',
        'panData':      'descend',
        'paTRID':       'descend',
        'paDate':       'set',
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
        'trStatus':     'set',
        'reID':         'set',
        'reDate':       'set',
        'acID':         'set',
        'acDate':       'set',
    }

    CONTACT_TYPES = (
        'admin',
        'tech',
        'billing'
    )

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'domain'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

    def parse_hostObj(self, response, tag):
        response.put_to_list('nss', tag.text.lower())

    def parse_host(self, response, tag):
        response.put_to_list('hosts', tag.text.lower())

    def parse_contact(self, response, tag):
        response.set(tag.attrib['type'], tag.text)

### REQUEST rendering

    def render_check(self, request, data):
        command = self.render_command(request, 'check')
        for name in data.get('names', []):
            request.add_subtag(command, 'domain:name', text=name)

    def render_info(self, request, data):
        hosts = data.get('hosts', 'all')
        command = self.render_command_with_fields(request, 'info', [
            TagData('name', data.get('name'), {'hosts': hosts})
        ])
        if 'pw' in data:
            self.render_auth_info(request, command, data['pw'])

    def render_transfer(self, request, data):
        attrs = {'op': data.get('op') or 'request'}

        command = self.render_command_with_fields(request, 'transfer', [
            TagData('name', data.get('name')),
            TagData('period', data.get('period'), {'unit': 'y'}),
        ], attrs)

        if 'pw' in data or attrs.get('op') == 'request':
            roid = {'roid': data.get('roid')} if 'roid' in data else {}
            self.render_auth_info(request, command,  data.get('pw'), roid)

    def render_create(self, request, data):
        command = self.render_command_with_fields(request, 'create', [
            TagData('name', data.get('name')),
            TagData('period', data.get('period'), {'unit': 'y'}),
        ])

        if 'nss' in data:
            self.render_nss(request, command, data.get('nss'))
        if 'registrant' in data:
            request.add_subtag(command, 'domain:registrant', {}, data.get('registrant'))

        if self.has_contacts(data):
            self.render_contacts(request, command, data)
        self.render_auth_info(request, command, data.get('pw'))

    def render_delete(self, request, data):
        self.render_command_with_fields(request, 'delete', [
            TagData('name', data.get('name'))
        ])

    def render_renew(self, request, data):
        self.render_command_with_fields(request, 'renew', [
            TagData('name', data.get('name')),
            TagData('curExpDate', data.get('curExpDate')),
            TagData('period', data.get('period'), {'unit': 'y'}),
        ])

    def render_update(self, request, data):
        command = self.render_command_with_fields(request, 'update', [
            TagData('name', data.get('name'))
        ])

        if 'add' in data:
            self.render_update_section(request, data, command, 'add')

        if 'rem' in data:
            self.render_update_section(request, data, command, 'rem')

        if 'chg' in data:
            chg_element = request.add_subtag(command, 'domain:chg')
            chg_data = data['chg']
            if 'registrant' in chg_data:
                request.add_subtag(chg_element, 'domain:registrant', text=chg_data['registrant'])
            if 'pw' in chg_data:
                self.render_auth_info(request, chg_element, chg_data.get('pw'))

    def render_restore(self, request, data):
        command = self.render_command_with_fields(request, 'update', [
            TagData('name', data.get('name'))
        ])
        request.add_subtag(command, 'domain:chg')

    def render_update_section(self, request, data, command, operation):
        element = request.add_subtag(command, 'domain:' + operation)
        data = data.get(operation)
        values = {}
        for d in data:
            if 'nss' in d:
                self.render_nss(request, element, d['nss'])
            if self.has_contacts(d):
                self.render_contacts(request, element, d)
            if 'statuses' in d:
                self.render_statuses(request, element, d['statuses'])

    def render_nss(self, request, parent, hosts):
        ns_element = request.add_subtag(parent, 'domain:ns')
        return self.render_multiple(request, ns_element, 'domain:hostObj', hosts)


    def render_contacts(self, request, parent, storage):
        for contact_type in (set(self.CONTACT_TYPES) & set(storage.keys())):
            self.render_multiple(request, parent, 'domain:contact', storage[contact_type], {'type': contact_type})

    def has_contacts(self, storage):
        return any(contact_type in storage for contact_type in self.CONTACT_TYPES)
