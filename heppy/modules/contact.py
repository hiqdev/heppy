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
        postalInfo = request.sub(command, 'contact:postalInfo', {'type': 'int'})
        request.sub(postalInfo, 'contact:name', text=request.get('name'))

        if request.has('org'):
            request.sub(postalInfo, 'contact:org', text=request.get('org'))

        self.render_addr(request, postalInfo)

        if request.has('voice'):
            request.sub(command, 'contact:voice', text=request.get('voice'))

        if request.has('fax'):
            request.sub(command, 'contact:fax', text=request.get('fax'))

        request.sub(command, 'contact:email', text=request.get('email'))
        if request.has('pw'):
            self.render_auth_info(request, command)

        if request.has('disclosure'):
            request.sub(command, 'contact:fax', text=request.get('fax'))

    def render_addr(self, request, command):
        addr = request.sub(command, 'contact:addr')

        if request.has('street1'):
            request.sub(addr, 'contact:street', text=request.get('street1'))
        if request.has('street2'):
            request.sub(addr, 'contact:street', text=request.get('street2'))
        if request.has('street3'):
            request.sub(addr, 'contact:street', text=request.get('street3'))

        request.sub(addr, 'contact:city', text=request.get('city'))

        if request.has('sp'):
            request.sub(addr, 'contact:sp', text=request.get('sp'))
        if request.has('pc'):
            request.sub(addr, 'contact:pc', text=request.get('pc'))
        request.sub(addr, 'contact:cc', text=request.get('cc'))
