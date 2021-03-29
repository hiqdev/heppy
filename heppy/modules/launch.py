from ..Module import Module
from ..TagData import TagData
from pprint import pprint

### https://tools.ietf.org/html/rfc8334

class launch(Module):
    opmap = {
        'chkData':      'descend',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'launch'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

    def parse_infData(self, response, tag):
        response.put_extension_block(response, 'launch:info', tag, {
            'currency': [],
            'price':      [],
            'period':   ['unit'],
        })

    def parse_delData(self, response, tag):
        self.parse_typical_tag(response, tag, 'price:delete')

    def parse_trnData(self, response, tag):
        self.parse_typical_tag(response, tag, 'price:transfer')

    def parse_creData(self, response, tag):
        self.parse_typical_tag(response, tag, 'price:create')

    def parse_renData(self, response, tag):
        self.parse_typical_tag(response, tag, 'price:renew')

    def parse_updData(self, response, tag):
        self.parse_typical_tag(response, tag, 'price:update')

    def parse_typical_tag(self, response, tag, command):
        response.put_extension_block(response, command, tag, {
            'currency': [],
            'price':    [],
            'period':   [],
        })

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
        ### XXX TODO
        pass

