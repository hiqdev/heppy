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
        chkData = {}
        chkData['command'] = 'fee:check'
        response.put_tag_data(chkData, tag, 'fee:domain')
        response.put_tag_data(chkData, tag, 'fee:currency')
        response.put_tag_data(chkData, tag, 'fee:action', [
            'phase',
            'subphase',
        ])
        response.put_tag_data(chkData, tag, 'fee:period', [
            'unit'
        ])
        response.put_tag_data(chkData, tag, 'fee:fee')

        response.put_to_list('extensions', chkData)

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

