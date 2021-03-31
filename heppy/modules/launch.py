from ..Module import Module
from ..TagData import TagData
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
        request.add_subtag(ext, 'launch:phase', {}, data.get('phase', 'claims'))

    def render_info(self, request, data):
        pass

    def render_create(self, request, data):
        ext = self.render_extension(request, 'create')
        request.add_subtag(ext, 'launch:phase', {}, data.get('phase', 'claims'))
        if 'code_mark' in data:
            self.render_code_mark(ext, request, data.get('code_mark'))
        if 'signed_mark' in data:
            self.render_signed_mark(ext, request, data.get('signed_mark'))
        if 'encoded_signed_mark' in data:
            self.render_encoded_signed_mark(ext, request, data.get('encoded_signed_mark'))
        if 'mark' in data:
            self.render_mark(ext, request, data.get('encoded_signed_mark'))

    def render_code_mark(self, parent, request, code):
        tag = request.add_subtag(parent, 'launch:codeMark')
        request.add_subtag(tag, 'launch:code', {}, code)

    def render_signed_mark(self, parent, request, code):
        return request.get_module('smd').render_signed_mark(parent, request, code)

    def render_encoded_signed_mark(self, parent, request, code):
        return request.get_module('smd').render_encoded_signed_mark(parent, request, code)

    def render_mark(self, parent, request, code):
        tag = request.add_subtag(parent, 'launch:codeMark', data)
        return request.get_module('mark').render_mark(tag, request, code)

