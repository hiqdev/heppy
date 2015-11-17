import xml.etree.ElementTree as ET

from pprint import pprint

def build(name, data):
    type = globals()[name]
    return type(data)

class Error(Exception):
    def __init__(self, message, data = {}):
        self.message = message
        self.data = data
    def __str__(self):
        return self.message + ": " + repr(self.data)

class Response:
    nsmap = {
        'epp':      'urn:ietf:params:xml:ns:epp-1.0',
        'domain':   'urn:ietf:params:xml:ns:domain-1.0',
    }

    okcodes = {
        '1000':     'completed',
        '1001':     'pending',
        '1300':     'no messages',
        '1301':     'ack to dequeue',
        '1500':     'ending session',
    }

    def __init__(self, xml):
        self.data       = {}
        self.root       = ET.fromstring(xml)
        self.response   = self.find(self.root,      'epp:response')
        self.result     = self.find(self.response,  'epp:result')
        self.trID       = self.find(self.response,  'epp:trID');
        self.resultMsg  = self.find(self.result,    'epp:msg')
        self.data['resultCode']     = self.result.attrib['code']
        self.data['resultLang']     = self.resultMsg.attrib['lang']
        self.data['resultMessage']  = self.resultMsg.text;
        self.data['cltrid']         = self.find(self.trID, 'epp:clTRID').text;
        self.data['svtrid']         = self.find(self.trID, 'epp:svTRID').text;
        if not self.data['resultCode'] in self.okcodes:
            raise Error(self.data['resultMessage'], self.data)
        self.resData    = self.find(self.response, 'epp:resData');

    def find(self, el, name):
        return el.find(name, namespaces=self.nsmap)

    def findall(self, el, name):
        return el.findall(name, self.nsmap)

class DomainCheck(Response):
    def __init__(self, xml):
        Response.__init__(self, xml)
        self.chkData        = self.find(self.resData, 'domain:chkData')
        self.data['avail']  = {}
        self.data['reason'] = {}
        for cd in self.findall(self.chkData, 'domain:cd'):
            name    = self.find(cd, 'domain:name')
            reason  = self.find(cd, 'domain:reason')
            self.data['avail'][name.text] = name.attrib['avail']
            if reason is not None:
                self.data['reason'][name.text] = reason.text

