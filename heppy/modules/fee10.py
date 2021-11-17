from ..Module import Module
from ..TagData import TagData
from pprint import pprint
from fee import fee


class fee10(fee):
    opmap = {
        'chkData':      'descend',
        'currency':     'set',
        'objID':        'set',
        'class':        'set',
        'fee':          'set',
        'command':      'descend',
        'period':       'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'fee'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

    def parse_infData(self, response, tag):
        response.put_extension_block(response, 'fee:info', tag, {
            'currency': [],
            'fee':      [],
            'action':   ['phase', 'subphase'],
            'period':   ['unit'],
        })

    def parse_delData(self, response, tag):
        response.put_extension_block(response, 'fee:delete', tag, {
            'currency': [],
            'credit':   [],
        })

    def parse_trnData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:transfer')

    def parse_creData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:create')

    def parse_renData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:renew')

    def parse_updData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:update')

    def parse_typical_tag(self, response, tag, command):
        response.put_extension_block(response, command, tag, {
            'currency': [],
            'fee':      [],
        })

### REQUEST rendering

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency',  {}, data.get('currency', 'USD'))
        create_command = request.add_subtag(ext, 'fee:command', {'name': 'create'})
        request.add_subtag(create_command, 'fee:period', {'unit': 'y'}, 1)
#        request.add_subtag(ext, 'fee:command', {'name':'renew'})
#        request.add_subtag(ext, 'fee:command', {'name':'transfer'})
#        request.add_subtag(ext, 'fee:command', {'name':'restore'})

    def render_info(self, request, data):
        self.render_extension_with_fields(request, 'info', [
            TagData('currency', data.get('currency')),
            TagData('command', data.get('action', 'create'), {
                'phase': data.get('phase'),
                'subphase': data.get('subphase'),
            }),
            TagData('period', data.get('period', 1), {
               'unit': data.get('unit', 'y')
            }),
        ])

    def render_create(self, request, data):
        self.render_extension_with_fields(request, 'create', [
            TagData('currency', data.get('currency')),
            TagData('fee', data.get('fee'))
        ])

    def render_renew(self, request, data):
        self.render_extension_with_fields(request, 'renew', [
            TagData('currency', data.get('currency')),
            TagData('fee', data.get('fee')),
        ])

    def render_transfer(self, request, data):
        self.render_extension_with_fields(request, 'transfer', [
            TagData('currency', data.get('currency')),
            TagData('fee', data.get('fee')),
        ])


