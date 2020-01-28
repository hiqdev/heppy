from fee import fee

class fee09(fee):
<<<<<<< HEAD
=======
    def __init__(self, xmlns):
        fee.__init__(self, xmlns)

### REQUEST rendering
>>>>>>> change constructor
    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        domain = request.add_subtag(ext, 'fee:object', {'objURI': data.get('objURI', 'urn:ietf:params:xml:ns:domain-1.0')})
        request.add_subtag(domain, 'fee:objID',     {'element':'name'}, data.get('name'))
        request.add_subtag(domain, 'fee:currency',  {},                 data.get('currency'))
        request.add_subtag(domain, 'fee:command',   {'phase': data.get('phase', 'claims')}, data.get('action'))
        request.add_subtag(domain, 'fee:period',    {'unit':'y'},       data.get('period'))
