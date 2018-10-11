from ..Module import Module
from ..TagData import TagData


class fee(Module):
    opmap = {
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

    def parse_chkData(self, response, tag):
        response.put_extension_block(response, 'fee:check', tag, {
            'domain':   [],
            'currency': [],
            'fee':      [],
            'action':   ['phase', 'subphase'],
            'period':   ['unit'],
        })

    def parse_infData(self, response, tag):
        response.put_extension_block(response, 'fee:info', tag, {
            'currency': [],
            'fee':      [],
            'action':   ['phase', 'subphase'],
            'period':   ['unit'],
        })

    def parse_trnData(self, response, tag):
        response.put_extension_block(response, 'fee:transfer', tag, {
            'currency': [],
            'fee':      [],
        })

    def parse_creData(self, response, tag):
        response.put_extension_block(response, 'fee:create', tag, {
            'currency': [],
            'fee':      [],
        })

    def parse_delData(self, response, tag):
        response.put_extension_block(response, 'fee:delete', tag, {
            'currency': [],
            'credit':   [],
        })

    def parse_renData(self, response, tag):
        response.put_extension_block(response, 'fee:renew', tag, {
            'currency': [],
            'fee':      [],
        })

    def parse_updData(self, response, tag):
        response.put_extension_block(response, 'fee:update', tag, {
            'currency': [],
            'fee':      [],
        })

### REQUEST rendering

    def render_check(self, request, data):
        self.render_extension_with_fields(request, 'check', [
            TagData('domain', data.get('name')),
            TagData('currency', data.get('currency')),
            TagData('action', data.get('action', 'create'), {
                'phase': data.get('phase'),
                'subphase': data.get('subphase'),
            }),
            TagData('period', data.get('period'), {
               'unit': data.get('unit', 'y')
            }),
        ])

    def render_info(self, request, data):
        self.render_extension_with_fields(request, 'info', [
            TagData('currency', data.get('currency')),
            TagData('action', data.get('action', 'create'), {
                'phase': data.get('phase'),
                'subphase': data.get('subphase'),
            }),
            TagData('period', data.get('period'), {
               'unit': data.get('unit', 'y')
            }),
        ])

    def render_create(self, request, data):
        self.render_extension_with_fields(request, 'create', [
            TagData('currency', data.get('currency')),
            TagData('fee', data.get('fee'))
        ])

