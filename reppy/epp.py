from Module import Module

class epp(Module):
    opmap = {
        'greeting':     'descend',
        'response':     'descend',
        'extension':    'descend',
        'svcMenu':      'nothing',
        'dcp':          'nothing',
        'svID':         'set',
        'svDate':       'set',
        'value':        'descend',
        'extValue':     'descend',
        'undef':        'nothing',
        'trID':         'descend',
        'clTRID':       'set',
        'svTRID':       'set',
        'resData':      'descend',
    }

    def parse_result(self, tag):
        self.set('result.code', tag.attrib['code'])
        self.parse_descend(tag)

    def parse_msg(self, tag):
        if 'lang' in tag.attrib:
            self.set('result.lang', tag.attrib['lang'])
        self.set('result.msg', tag.text)

    def parse_reason(self, tag):
        self.set('result.reason', tag.text)

