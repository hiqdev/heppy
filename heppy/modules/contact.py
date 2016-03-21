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

