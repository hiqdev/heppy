from Module import Module

class epp(Module):
    opmap = {
        'greeting':     'descend',
        'response':     'descend',
        'extension':    'descend',
        'svcMenu':      'nothing',
        'dcp':          'nothing',
        'svID':         'set',
        'svDate':       'set',
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
        response.set('result.code', tag.attrib['code'])
        self.parse_descend(response, tag)

    def parse_msg(self, response, tag):
        if 'lang' in tag.attrib:
            response.set('result.lang', tag.attrib['lang'])
        response.set('result.msg', tag.text)

    def parse_reason(self, response, tag):
        response.set('result.reason', tag.text)

### REQUEST rendering

    def render_login(self, request):
        action = self.render_root_command(request, 'login')
        request.sub(action, 'clID', {}, request.get('clID', request.get('login')))
        request.sub(action, 'pw',   {}, request.get('pw',   request.get('password')))
        newPW = request.get('newPW', request.get('newPassword'))
        if newPW is not None:
            request.sub(action, 'newPW', {}, newPW)
        options = request.sub(action, 'options')
        request.sub(options, 'version', {}, request.get('version', '1.0'))
        request.sub(options, 'lang',    {}, request.get('lang', 'en'))
        svcs = request.sub(action, 'svcs')
        for svc in request.get('svcs', [request.nsmap['epp']]):
            request.sub(svcs, 'objURI', {}, svc)

    def render_logout(self, request):
        self.render_root_command(request, 'logout')

    def render_poll(self, request):
        attrs = {'op': request.get('op', 'req')}
        msgID = request.get('msgID')
        if msgID is not None:
            attrs['msgID'] = msgID
        self.render_root_command(request, 'poll', attrs)
