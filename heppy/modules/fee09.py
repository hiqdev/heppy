from fee import fee

class fee09(fee):
#   PARSE
    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag, 'objID')

# RENDER
    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        domain = request.add_subtag(ext, 'fee:object', {'objURI': data.get('objURI', 'urn:ietf:params:xml:ns:domain-1.0')})
        request.add_subtag(domain, 'fee:objID',     {'element':'name'}, data.get('name'))
        request.add_subtag(domain, 'fee:currency',  {},                 data.get('currency', 'USD'))
        request.add_subtag(domain, 'fee:command',   {},                 data.get('action', 'create'))
        request.add_subtag(domain, 'fee:period',    {'unit':'y'},       data.get('period', '1'))
