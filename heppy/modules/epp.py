from ..Module import Module

class epp(Module):
    opmap = {
        'greeting':     'descend',
        'response':     'descend',
        'extension':    'descend',
        'svcMenu':      'descend',
        'svcExtension': 'descend',
        'dcp':          'nothing',
        'svID':         'set',
        'svDate':       'set',
        'lang':         'set',
        'version':      'set',
        'objURI':       'add_list',
        'extURI':       'add_list',
        'value':        'descend',
        'extValue':     'descend',
        'undef':        'nothing',
        'trID':         'descend',
        'clTRID':       'set',
        'svTRID':       'set',
        'resData':      'descend',
    }

### RESPONSE parsing

    def parse_result(self, response, tag):
        response.set('result_code', tag.attrib['code'])
        self.parse_descend(response, tag)

    def parse_msg(self, response, tag):
        if 'lang' in tag.attrib:
            response.set('result_lang', tag.attrib['lang'])
        response.set('result_msg', tag.text)

    def parse_reason(self, response, tag):
        response.set('result_reason', tag.text)

### REQUEST rendering

    def render_hello(self, request):
        epp = self.render_epp(request)
        request.add_subtag(epp, 'hello')

    def render_login(self, request):
        command = self.render_root_command(request, 'login')

        request.add_subtag(command, 'clID', text=request.get('clID', request.get('login')))
        request.add_subtag(command, 'pw', text=request.get('pw', request.get('password')))
        newPW = request.get('newPW', request.get('newPassword'))
        if newPW is not None:
            request.add_subtag(command, 'newPW', text=newPW)

        options = request.add_subtag(command, 'options')
        request.add_subtag(options, 'version', text=request.get('version', '1.0'))
        request.add_subtag(options, 'lang', text=request.get('lang', 'en'))

        svcs = request.add_subtag(command, 'svcs')
        for svc in request.get('objURIs', [request.nsmap['epp']]):
            request.add_subtag(svcs, 'objURI', text=svc)
        extURIs = request.get('extURIs', [])
        if extURIs:
            exts = request.add_subtag(svcs, 'svcExtension')
            for ext in extURIs:
                request.add_subtag(exts, 'extURI', text=ext)

    def render_logout(self, request):
        self.render_root_command(request, 'logout')

    def render_check(self, request):
        self.render_typical_command(request, 'check')

    def render_info(self, request):
        self.render_typical_command(request, 'info')

    def render_poll(self, request):
        attrs = {'op': request.get('op', 'req')}
        msgID = request.get('msgID')
        if msgID is not None:
            attrs['msgID'] = msgID
        self.render_root_command(request, 'poll', attrs)

    def render_typical_command(self, request, command_name):
        command = self.render_root_command(request, command_name)
        objs = request.add_subtag(command, 'obj:' + command_name, {'xmlns:obj': 'urn:ietf:params:xml:ns:obj'})
        for name in request.get('names'):
            request.add_subtag(objs, 'obj:name', text=name)
