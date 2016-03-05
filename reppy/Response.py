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
        '{urn:ietf:params:xml:ns:epp-1.0}extension':    'elements',
        '{urn:ietf:params:xml:ns:epp-1.0}result':       'result',
        '{urn:ietf:params:xml:ns:epp-1.0}value':        'elements',
        '{urn:ietf:params:xml:ns:epp-1.0}extValue':     'elements',
        '{urn:ietf:params:xml:ns:epp-1.0}undef':        'nothing',
        '{urn:ietf:params:xml:ns:epp-1.0}reason':       'result_reason',
        '{urn:ietf:params:xml:ns:epp-1.0}msg':          'result_msg',
        '{urn:ietf:params:xml:ns:epp-1.0}trID':         'elements',
        '{urn:ietf:params:xml:ns:epp-1.0}clTRID':       'clTRID',
        '{urn:ietf:params:xml:ns:epp-1.0}svTRID':       'svTRID',
        '{urn:ietf:params:xml:ns:epp-1.0}resData':      'elements',
        '{urn:ietf:params:xml:ns:domain-1.0}chkData':   'domainCheck',
        '{urn:ietf:params:xml:ns:domain-1.0}infData':   'domainInfo',

        ### oxrs
        '{urn:afilias:params:xml:ns:oxrs-1.1}xcp':      'result_reason',

        ### fee extension
        '{urn:ietf:params:xml:ns:fee-0.7}chkData':      'feeCheck',

        ### rgp
        '{urn:ietf:params:xml:ns:rgp-1.0}infData':      'elements',
        '{urn:ietf:params:xml:ns:rgp-1.0}rgpStatus':    'rgp_status',
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

    def parse_nothing(self, elements):
        pass

    def parse_elements(self, elements):
        for tag in elements:
            self.parse(tag)
            
    def parse_result(self, result):
        self.data['result'] = {}
        self.data['result']['code'] = result.attrib['code']
        for tag in result:
            self.parse(tag)

    def parse_result_msg(self, msg):
        if 'lang' in msg.attrib:
            self.data['result']['lang'] = msg.attrib['lang']
        self.data['result']['message'] = msg.text

    def parse_result_reason(self, data):
        self.data['result']['reason'] = data.text

    def parse_clTRID(self, clTRID):
        self.data['cltrid'] = clTRID.text

    def parse_svTRID(self, svTRID):
        self.data['svtrid'] = svTRID.text

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
        self.data['name']           = self.find(data, 'domain:name').text
        self.data['created_date']   = self.find(data, 'domain:crDate').text
        self.data['expiration_date']= self.find(data, 'domain:exDate').text

    def parse_domainInfo(self, data):
        self.data['name']           = self.find(data, 'domain:name').text
        self.data['created_date']   = self.find(data, 'domain:crDate').text
        self.data['updated_date']   = self.find(data, 'domain:upDate').text
        self.data['expiration_date']= self.find(data, 'domain:exDate').text
        self.data['password']       = self.find(self.find(data, 'domain:authInfo'), 'domain:pw').text

    def parse_rgp_status(self, data):
        status = data.attrib['s']
        self.data[status] = data.text
