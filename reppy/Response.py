import xml.etree.ElementTree as ET

from reppy.Error import Error
from pprint import pprint

class Response:
    nsmap = {
        'epp':      'urn:ietf:params:xml:ns:epp-1.0',
        'domain':   'urn:ietf:params:xml:ns:domain-1.0',
        'oxrs':     'urn:afilias:params:xml:ns:oxrs-1.1',
        'fee':      'urn:ietf:params:xml:ns:fee-0.7',
    }

    tagmap = {
        '{urn:ietf:params:xml:ns:epp-1.0}greeting':     'greeting',
        '{urn:ietf:params:xml:ns:epp-1.0}response':     'elements',
        '{urn:ietf:params:xml:ns:epp-1.0}result':       'result',
        '{urn:ietf:params:xml:ns:epp-1.0}trID':         'trID',
        '{urn:ietf:params:xml:ns:epp-1.0}value':        'value',
        '{urn:ietf:params:xml:ns:epp-1.0}resData':      'elements',
        '{urn:ietf:params:xml:ns:domain-1.0}chkData':   'domainCheck',
        '{urn:ietf:params:xml:ns:epp-1.0}extension':    'elements',
        '{urn:ietf:params:xml:ns:fee-0.7}chkData':      'feeCheck',
    }

    okcodes = {
        '1000':     'completed',
        '1001':     'pending',
        '1300':     'no messages',
        '1301':     'ack to dequeue',
        '1500':     'ending session',
    }

    @staticmethod
    def parsexml(xml):
        root = ET.fromstring(xml)
        return Response(root)

    @staticmethod
    def build(name, start):
        type = globals()[name]
        return type(start)

    def find(self, el, name):
        return el.find(name, namespaces=self.nsmap)

    def findall(self, el, name):
        return el.findall(name, self.nsmap)

    def __init__(self, root):
        self.data = {}
        self.root = root
        self.parse(self.root[0])

    def parse(self, tag):
        method = self.tagmap.get(tag.tag)
        if method is None:
            raise Exception('unknown tag', tag.tag)
        getattr(self, 'parse_' + method)(tag)

    def parse_greeting(self, greeting):
        self.data['svid']   = self.find(greeting, 'epp:svID').text
        self.data['svdate'] = self.find(greeting, 'epp:svDate').text
        pass

    def parse_elements(self, elements):
        for tag in elements:
            self.parse(tag)
            
    def parse_result(self, result):
        resultMsg  = self.find(result, 'epp:msg')
        self.data['result'] = {}
        self.data['result']['code']    = result.attrib['code']
        self.data['result']['lang']    = resultMsg.attrib['lang']
        self.data['result']['message'] = resultMsg.text
        value = self.find(result, 'epp:value')
        if value is not None:
            self.parse(value)

    def parse_value(self, value):
        self.xcp = self.find(value, 'oxrs:xcp')
        self.data['result']['extendedMessage'] = self.xcp.text

    def parse_trID(self, trID):
        self.data['cltrid'] = self.find(trID, 'epp:clTRID').text
        self.data['svtrid'] = self.find(trID, 'epp:svTRID').text

    def parse_domainCheck(self, chkData):
        self.data['avail']  = {}
        self.data['reason'] = {}
        for cd in chkData:
            name    = self.find(cd, 'domain:name')
            reason  = self.find(cd, 'domain:reason')
            self.data['avail'][name.text] = name.attrib['avail']
            if reason is not None:
                self.data['reason'][name.text] = reason.text

    def parse_feeCheck(self, chkData):
        fees = {}
        if not 'FeeCheck' in self.data:
            self.data['FeeCheck'] = {}
        for cd in chkData:
            fee = {}
            periodTag = self.find(cd, 'fee:period')
            feeTag    = self.find(cd, 'fee:fee')
            fee['name']         = self.find(cd, 'fee:name').text
            fee['command']      = self.find(cd, 'fee:command').text
            fee['currency']     = self.find(cd, 'fee:currency').text
            fee['class']        = self.find(cd, 'fee:class').text
            fee['period']       = periodTag.text
            fee['unit']         = periodTag.attrib['unit']
            fee['fee']          = feeTag.text
            fee['description']  = feeTag.attrib['description']
            fee['refundable']   = feeTag.attrib['refundable']
            fee['grace-period'] = feeTag.attrib['grace-period']
            self.data['FeeCheck'][fee['name']] = fee

    def parse_domainCreate(self, creData):
        self.data['name']           = self.find(creData, 'domain:name').text
        self.data['created_date']   = self.find(creData, 'domain:crDate').text
        self.data['expiration_date']= self.find(creData, 'domain:exDate').text

