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
        return self.render_check_command(request, 'host', 'name')

    def render_info(self, request):
        return self.render_command_fields(request, 'info', {'name': {}})

