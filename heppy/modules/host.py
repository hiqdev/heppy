from collections import OrderedDict

from ..Module import Module

class host(Module):
    opmap = {
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
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

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

    def parse_addr(self, response, tag):
        response.addpair('ips', tag.text)

### REQUEST rendering

    def render_check(self, request):
        self.render_check_command(request, 'host', 'name')

    def render_info(self, request):
        self.render_command_fields(request, 'info')

    def render_create(self, request):
        command = self.render_command_fields(request, 'create')
        self.render_ips(request, command)

    def render_delete(self, request):
        self.render_command_fields(request, 'delete')

    def render_update(self, request):
        command = self.render_command_fields(request, 'update')

        if request.has('add'):
            self.render_update_section(request, command, 'add')
        if request.has('rem'):
            self.render_update_section(request, command, 'rem')
        if request.has('chg'):
            self.render_update_section(request, command, 'chg')


    def render_update_section(self, request, command, operation):
        element = request.add_subtag(command, 'host:' + operation)
        data = request.get(operation)
        if operation == 'chg':
            request.add_subtag(element, 'host:name', text=data.get('name'))
        else:
            self.render_ips(request, element, data)
            self.render_statuses(request, element, data.get('statuses', {}))

    def render_ips(self, request, parent, storage=None):
        storage = storage or request.data
        for ip in storage.get('ips', []):
            request.add_subtag(parent, 'host:addr', {'ip': 'v6' if ':' in ip else 'v4'}, ip)
