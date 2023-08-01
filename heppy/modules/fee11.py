from fee import fee

class fee11(fee):
    opmap = {
        'chkData':      'descend',
        'currency':     'set',
        'class':        'set',
        'fee':          'set',
        'command':      'set',
        'period':       'set',
    }

    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

    def parse_object(self, response, tag):
        return response

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:command',   {},             data.get('action', 'create'))
        request.add_subtag(ext, 'fee:currency',  {},             data.get('currency', 'USD'))
#        request.add_subtag(ext, 'fee:period',    {'unit':'y'},   data.get('period', 1))
