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
        extension_data = request.extension_data
        self.render_name(request, extension, extension_data)
        self.render_currency(request, extension, extension_data)
        self.render_action(request, extension, extension_data)
        self.render_period(request, extension, extension_data)

    def render_name(self, request, extension, extension_data):
        if 'name' in extension_data:
            request.add_subtag(extension, 'fee:domain', text=extension_data['name'])

    def render_currency(self, request, extension, extension_data):
        if 'currency' in extension_data:
            request.add_subtag(extension, 'fee:currency', text=extension_data['currency'])

    def render_action(self, request, extension, extension_data):
        action = extension_data.get('action', 'create')

        attrs = {}
        phase = extension_data.get('phase', None)
        if phase:
            attrs['phase'] = phase
        subphase = extension_data.get('subphase', None)
        if subphase:
            attrs['subphase'] = subphase

        request.add_subtag(extension, 'fee:action', attrs, action)

    def render_period(self, request, extension, extension_data):
        if 'period' in extension_data:
            request.add_subtag(extension, 'fee:period', {
                'unit': extension_data.get('unit', 'y')
            }, extension_data['currency'])

    def render_create(self, request):
        return self.render_action(request, 'create')

    def render_renew(self, request):
        return self.render_action(request, 'renew')

