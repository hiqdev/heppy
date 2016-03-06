from Module import Module

class fee(Module):
    opmap = {
        'chkData':      'descend',
    }

    def parse_cd(self, tag):
        fee = {}
        periodTag = self.find(tag, 'fee:period')
        feeTag    = self.find(tag, 'fee:fee')
        fee['name']         = self.find(tag, 'fee:name').text
        fee['command']      = self.find(tag, 'fee:command').text
        fee['currency']     = self.find(tag, 'fee:currency').text
        fee['class']        = self.find(tag, 'fee:class').text
        fee['period']       = periodTag.text
        fee['unit']         = periodTag.attrib['unit']
        fee['fee']          = feeTag.text
        fee['description']  = feeTag.attrib['description']
        fee['refundable']   = feeTag.attrib['refundable']
        fee['grace-period'] = feeTag.attrib['grace-period']

        fees = self.response.get('FeeCheck', {})
        fees[fee['name']] = fee
        self.set('FeeCheck', fees)
