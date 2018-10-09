from ..Module import Module
from ..TagData import TagData

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

    def render_check(self, request, data):
        return self.render_check_command(request, data, 'id')

    def render_info(self, request, data):
        command = self.render_command_with_fields(request, 'info', [
            TagData('id', data.get('id'))
        ])
        if 'pw' in data:
            self.render_auth_info(request, command, data.get('pw'))

    def render_create(self, request, data):
        command = self.render_command_with_fields(request, 'create', [
            TagData('id', data.get('id'))
        ])

        self.render_postal_info(request, data, command)
        self.render_contact_info(request, data, command)

        if 'pw' in data:
            self.render_auth_info(request, command, data.get('pw'))

    def render_delete(self, request, data):
        self.render_command_with_fields(request, 'delete', [
            TagData('id', data.get('id'))
        ])

    def render_update(self, request, data):
        command = self.render_command_with_fields(request, 'update', [
            TagData('id', data.get('id'))
        ])

        if 'add' in data:
            self.render_update_section(request, data, command, 'add')
        if 'rem' in data:
            self.render_update_section(request, data, command, 'rem')
        if 'chg' in data:
            chg = request.add_subtag(command, 'contact:chg')
            chgData = data.get('chg')
            self.render_postal_info(request, chgData, chg)
            self.render_contact_info(request, chgData, chg)
            if 'pw' in chgData:
                self.render_auth_info(request, chg, chgData['pw'])

    def render_update_section(self, request, data, command, operation):
        element = request.add_subtag(command, 'contact:' + operation)
        data = data.get(operation)
        if 'statuses' in data:
            self.render_statuses(request, element, data['statuses'])

    def render_postal_info(self, request, data, parent):
        attrs = {'type': data.get('type', 'int')}
        postalInfo = request.add_subtag(parent, 'contact:postalInfo', attrs)
        if 'name' in data:
            request.add_subtag(postalInfo, 'contact:name', text=data.get('name'))
        if 'org' in data:
            request.add_subtag(postalInfo, 'contact:org', text=data.get('org'))
        self.render_addr(request, postalInfo, data)

    def render_addr(self, request, parent, data):
        addr = request.add_subtag(parent, 'contact:addr')

        if 'street1' in data:
            request.add_subtag(addr, 'contact:street', text=data.get('street1'))
        if 'street2' in data:
            request.add_subtag(addr, 'contact:street', text=data.get('street2'))
        if 'street3' in data:
            request.add_subtag(addr, 'contact:street', text=data.get('street3'))

        if 'city' in data:
            request.add_subtag(addr, 'contact:city', text=data.get('city'))

        if 'sp' in data:
            request.add_subtag(addr, 'contact:sp', text=data.get('sp'))
        if 'pc' in data:
            request.add_subtag(addr, 'contact:pc', text=data.get('pc'))
        request.add_subtag(addr, 'contact:cc', text=data.get('cc'))

    def render_contact_info(self, request, data, parent):
        if 'voice' in data:
            request.add_subtag(parent, 'contact:voice', text=data.get('voice'))
        if 'fax' in data:
            request.add_subtag(parent, 'contact:fax', text=data.get('fax'))
        if 'email' in data:
            request.add_subtag(parent, 'contact:email', text=data.get('email'))
