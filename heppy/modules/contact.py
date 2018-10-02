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
        postalInfo = request.add_subtag(command, 'contact:postalInfo', {'type': 'int'})
        request.add_subtag(postalInfo, 'contact:name', text=request.get('name'))

        if request.has('org'):
            request.add_subtag(postalInfo, 'contact:org', text=request.get('org'))

        self.render_addr(request, postalInfo)

        if request.has('voice'):
            request.add_subtag(command, 'contact:voice', text=request.get('voice'))

        if request.has('fax'):
            request.add_subtag(command, 'contact:fax', text=request.get('fax'))

        request.add_subtag(command, 'contact:email', text=request.get('email'))
        if request.has('pw'):
            self.render_auth_info(request, command)

    def render_addr(self, request, command):
        addr = request.add_subtag(command, 'contact:addr')

        if request.has('street1'):
            request.add_subtag(addr, 'contact:street', text=request.get('street1'))
        if request.has('street2'):
            request.add_subtag(addr, 'contact:street', text=request.get('street2'))
        if request.has('street3'):
            request.add_subtag(addr, 'contact:street', text=request.get('street3'))

        request.add_subtag(addr, 'contact:city', text=request.get('city'))

        if request.has('sp'):
            request.add_subtag(addr, 'contact:sp', text=request.get('sp'))
        if request.has('pc'):
            request.add_subtag(addr, 'contact:pc', text=request.get('pc'))
        request.add_subtag(addr, 'contact:cc', text=request.get('cc'))
