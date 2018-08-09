from ..Module import Module

class fee(Module):
    opmap = {
        'chkData':      'descend',
    }

### RESPONSE parsing

    def parse_cd(self, response, tag):
        fee = {}
        periodTag           = response.find(tag, 'fee:period')
        feeTag              = response.find(tag, 'fee:fee')
        fee['name']         = response.find(tag, 'fee:name').text
        fee['command']      = response.find(tag, 'fee:command').text
        fee['currency']     = response.find(tag, 'fee:currency').text
        fee['class']        = response.find(tag, 'fee:class').text
        fee['period']       = periodTag.text
        fee['unit']         = periodTag.attrib['unit']
        fee['fee']          = feeTag.text
        fee['description']  = feeTag.attrib['description']
        fee['refundable']   = feeTag.attrib['refundable']
        fee['grace-period'] = feeTag.attrib['grace-period']

        fees = response.get('fee:check', {})
        fees[fee['name']] = fee
        response.set('fee:check', fees)

### REQUEST rendering

    def render_check(self, request):
        extension = self.render_extension(request, 'check')
        command = request.get('fee', {}).get('command', 'create')
        for name in request.get('names').itervalues():
            domain = request.sub(extension, 'fee:domain')
            request.sub(domain, 'fee:name', {}, name)
            request.sub(domain, 'fee:command', {}, command)
            request.sub(domain, 'fee:period', {'unit': 'y'}, '1')

    def render_create(self, request):
        return self.render_action(request, 'create')

    def render_renew(self, request):
        return self.render_action(request, 'renew')

    def render_action(self, request, action):
        extension = self.render_extension(request, action)
        data = request.get('fee', {})
        request.sub(extension, 'fee:currency', {}, data.get('currency', 'USD'))
        request.sub(extension, 'fee:fee',      {}, data.get('fee'))
