# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData


class host(Module):
    opmap = {
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'panData':      'descend',
        'roid':         'set',
        'name':         'set',
        'clID':         'set',
        'crID':         'set',
        'upID':         'set',
        'crDate':       'set',
        'upDate':       'set',
        'exDate':       'set',
        'trDate':       'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'host'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

    def parse_addr(self, response, tag):
        response.put_to_list('ips', tag.text)

### REQUEST rendering

    def render_check(self, request, data):
        command = self.render_command(request, 'check')
        for name in data.get('names', []):
            request.add_subtag(command, 'host:name', text=name)

    def render_info(self, request, data):
        self.render_command_with_fields(request, 'info', [
            TagData('name', data.get('name'))
        ])

    def render_create(self, request, data):
        command = self.render_command_with_fields(request, 'create', [
            TagData('name', data.get('name'))
        ])
        if (data.get('ips', None) is not None) :
            self.render_ips(request, data.get('ips', []), command)

    def render_delete(self, request, data):
        self.render_command_with_fields(request, 'delete', [
            TagData('name', data.get('name'))
        ])

    def render_update(self, request, data):
        command = self.render_command_with_fields(request, 'update', [
            TagData('name', data.get('name'))
        ])

        if 'add' in data:
            self.render_update_section(request, data.get('add'), command, 'add')
        if 'rem' in data:
            self.render_update_section(request, data.get('rem'), command, 'rem')
        if 'chg' in data:
            self.render_update_section(request, data.get('chg'), command, 'chg')

    def render_update_section(self, request, data, command, operation):
        element = request.add_subtag(command, 'host:' + operation)
        if operation == 'chg':
            request.add_subtag(element, 'host:name', text=data.get('name'))
        else:
            for d in data:
                if 'ips' in d:
                    self.render_ips(request, d['ips'], element)
                if 'statuses' in d:
                    self.render_statuses(request, element, d['statuses'])

    def render_ips(self, request, ips, parent):
        if (isinstance(ips, list) == False):
            for ip in ips.values():
                request.add_subtag(parent, 'host:addr', {'ip': 'v6' if ':' in ip else 'v4'}, ip)
        else:
            for ip in ips:
                request.add_subtag(parent, 'host:addr', {'ip': 'v6' if ':' in ip else 'v4'}, ip)
