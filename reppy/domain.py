from collections import OrderedDict

from Module import Module

class domain(Module):
    opmap = {
        'greeting':     'descend',
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'ns':           'descend',
        'authInfo':     'descend',
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
    }

    def parse_cd(self, response, tag):
        avails  = response.get('avails', {})
        reasons = response.get('reasons', {})
        name    = response.find(tag, 'domain:name')
        reason  = response.find(tag, 'domain:reason')
        avails[name.text] = name.attrib['avail']
        if reason is not None:
            reasons[name.text] = reason.text
        response.set('avails',  avails)
        response.set('reasons', reasons)

    def parse_status(self, response, tag):
        status = tag.attrib['s']
        statuses = response.get('statuses', {})
        statuses[status] = status
        response.set('statuses', statuses)

    def parse_hostObj(self, response, tag):
        ns = tag.text.lower()
        nss = response.get('nss', {})
        nss[ns] = ns
        response.set('nss', nss)

    def parse_host(self, response, tag):
        host = tag.text.lower()
        hosts = response.get('hosts', {})
        hosts[host] = host
        response.set('hosts', hosts)

    def parse_contact(self, response, tag):
        response.set(tag.attrib['type'], tag.text)

### REQUEST rendering

    def render_check(self, request):
        action = self.render_command(request, 'check')
        for name in request.get('names').itervalues():
            request.sub(action, 'domain:name', {}, name)

    def render_info(self, request):
        self.render_command_fields(request, 'info', {'name': {'hosts': 'all'}})

    def render_create(self, request):
        command = self.render_command_fields(request, 'create', OrderedDict([
            ('name', {}),
            ('period', {'unit': 'y'}),
        ]))
        if request.get('registrant'):
            request.sub(command, 'domain:registrant', {}, request.get('registrant'))
        for type in ('admin', 'tech', 'billing'):
            if request.get(type):
                request.sub(command, 'domain:contact', {'type': type}, request.get(type))
        authInfo = request.sub(command, 'domain:authInfo')
        request.sub(authInfo, 'domain:pw', {}, request.get('pw', request.get('password', '')))

    def render_delete(self, request):
        self.render_command_fields(request, 'delete')

    def render_renew(self, request):
        self.render_command_fields(request, 'renew', OrderedDict([
            ('name', {}),
            ('curExpDate', {}),
            ('period', {'unit': 'y'}),
        ]))
