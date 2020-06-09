from ..Module import Module
from ..TagData import TagData
from pprint import pprint


class price(Module):
    opmap = {
        'chkData':      'descend',
    }
### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

    def parse_infData(self, response, tag):
        response.put_extension_block(response, 'price:info', tag, {
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
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'price:period',    {'unit':'y'}, data.get('period', 1))

    def render_info(self, request, data):
        pass

    def render_create(self, request, data):
        ext = self.render_extension(request, 'create')
        self.render_extension_with_fields(ext, 'ack', [
            TagData('price', data.get('price')),
            TagData('renewalPrice', data.get('renewalPrice'))
        ])

    def render_renew(self, request, data):
        ext = self.render_extension(request, 'renew')
        self.render_extension_with_fields(ext, 'ack', [
            TagData('renewalPrice', data.get('renewalPrice'))
        ])

    def render_transfer(self, request, data):
        ext = self.render_extension(request, 'transfer')
        self.render_extension_with_fields(ext, 'ack', [
            TagData('renewalPrice', data.get('renewalPrice'))
        ])


