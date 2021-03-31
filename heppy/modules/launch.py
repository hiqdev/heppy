from ..Module import Module
from ..TagData import TagData
from smd import smd
from pprint import pprint

### https://tools.ietf.org/html/rfc8334

class launch(Module):
    opmap = {
        'chkData':      'descend',
        'creData':      'descend',
        'notice':       'descend',
        'phase':        'set',
        'noticeID':     'set',
        'notAfter':     'set',
        'acceptedDate': 'set',

    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'launch'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

### REQUEST rendering

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check', {'type': data.get('type', 'claims')})
        request.add_subtag(ext, 'launch:phase', data.get('phase'))

    def render_info(self, request, data):
        pass

    def render_create(self, request, data):
        ext = self.render_extension(request, 'create')
        request.add_subtag(ext, 'launch:phase', data.get('phase'))
        for mark in data.get('code_marks', []):
            self.render_code_mark(request, mark, ext)

    def render_code_mark(self, request, data, tag):
        smd = smd()
        return smd.render_encodedSignedMark(request, ext, mark)

