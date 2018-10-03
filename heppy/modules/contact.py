from ..Module import Module

class contact(Module):
    opmap = {
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'authInfo':     'descend',
        'postalInfo':   'descend',
        'addr':         'descend',
        'id':           'set',
        'roid':         'set',
        'name':         'set',
        'org':          'set',
        'street':       'set',
        'city':         'set',
        'pc':           'set',
        'sp':           'set',
        'cc':           'set',
        'email':        'set',
        'voice':        'set',
        'fax':          'set',
        'clID':         'set',
        'crID':         'set',
        'upID':         'set',
        'crDate':       'set',
        'upDate':       'set',
        'trDate':       'set',
        'pw':           'set',
    }

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

### REQUEST rendering

    def render_check(self, request):
        return self.render_check_command(request, 'contact', 'id')

    def render_info(self, request):
        command = self.render_command_fields(request, 'info', {'id': {}})
        if request.has('pw'):
            self.render_auth_info(request, command)

    def render_create(self, request):
        command = self.render_command_fields(request, 'create', {'id': {}})

        self.render_postal_info(request, command)
        self.render_contact_info(request, command)

        if request.has('pw'):
            self.render_auth_info(request, command)

    def render_delete(self, request):
        self.render_command_fields(request, 'delete', {'id': {}})

    def render_update(self, request):
        command = self.render_command_fields(request, 'update', {'id': {}})

        if request.has('add'):
            self.render_update_section(request, command, 'add')
        if request.has('rem'):
            self.render_update_section(request, command, 'rem')
        if request.has('chg'):
            chg = request.add_subtag(command, 'contact:chg')
            chgData = request.get('chg')
            self.render_postal_info(request, chg, chgData)
            self.render_contact_info(request, chg, chgData)
            if 'pw' in chgData:
                self.render_auth_info(request, chg, chgData['pw'])

    def render_update_section(self, request, command, operation):
        element = request.add_subtag(command, 'contact:' + operation)
        data = request.data.get(operation)
        if 'statuses' in data:
            self.render_statuses(request, element, data['statuses'])

    def render_postal_info(self, request, parent, storage=None):
        storage = storage or request.data
        postalInfo = request.add_subtag(parent, 'contact:postalInfo',
                                        {'type': storage.get('type', 'int')})
        if 'name' in storage:
            request.add_subtag(postalInfo, 'contact:name', text=storage.get('name'))
        if 'org' in storage:
            request.add_subtag(postalInfo, 'contact:org', text=storage.get('org'))
        self.render_addr(request, postalInfo, storage)

    def render_addr(self, request, parent, storage=None):
        storage = storage or request.data
        addr = request.add_subtag(parent, 'contact:addr')

        if 'street1' in storage:
            request.add_subtag(addr, 'contact:street', text=storage.get('street1'))
        if 'street2' in storage:
            request.add_subtag(addr, 'contact:street', text=storage.get('street2'))
        if 'street3' in storage:
            request.add_subtag(addr, 'contact:street', text=storage.get('street3'))

        if 'city' in storage:
            request.add_subtag(addr, 'contact:city', text=storage.get('city'))

        if 'sp' in storage:
            request.add_subtag(addr, 'contact:sp', text=storage.get('sp'))
        if 'pc' in storage:
            request.add_subtag(addr, 'contact:pc', text=storage.get('pc'))
        request.add_subtag(addr, 'contact:cc', text=storage.get('cc'))

    def render_contact_info(self, request, parent, storage=None):
        storage = storage or request.data

        if 'voice' in storage:
            request.add_subtag(parent, 'contact:voice', text=storage.get('voice'))
        if 'fax' in storage:
            request.add_subtag(parent, 'contact:fax', text=storage.get('fax'))
        if 'email' in storage:
            request.add_subtag(parent, 'contact:email', text=storage.get('email'))
