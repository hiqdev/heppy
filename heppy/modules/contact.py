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
        request.sub(postalInfo, 'contact:name', {}, request.get('name'))
        request.sub(postalInfo, 'contact:org',  {}, request.get('org'))
        self.render_addr(request, postalInfo)
        request.sub(command, 'contact:voice',   {}, request.get('voice'))
        request.sub(command, 'contact:email',   {}, request.get('email'))
        if request.has('pw'):
            self.render_auth_info(request, command)

    def render_addr(self, request, command):
        addr = request.sub(command, 'contact:addr')
        request.sub(addr, 'contact:street', {}, request.get('street1'))
        request.sub(addr, 'contact:city',   {}, request.get('city'))
        if request.has('sp'):
            request.sub(addr, 'contact:sp', {}, request.get('sp'))
        request.sub(addr, 'contact:pc',     {}, request.get('pc'))
        request.sub(addr, 'contact:cc',     {}, request.get('cc'))

    def render_auth_info(self, request, command, pw = None):
        if pw is None:
            pw = request.get('pw', '')
        authInfo = request.sub(command, 'contact:authInfo')
        request.sub(authInfo, 'contact:pw', {}, pw)

