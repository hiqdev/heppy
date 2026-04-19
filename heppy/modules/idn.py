# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData

class idn(Module):
    opmap = {
        'infData': 'descend',
        'data': 'descend',
        'table': 'set',
        'uname': 'set',
        'language': 'set',
    }

### RESPONSE parsing

    def parse_infData(self, response, tag):
        response.put_extension_block(response, 'idn:info', tag, {
            'table': [],

        })

### REQUEST rendering

    def render_default(self, request, data):
        return self.render_data(request, data)

    def render_data(self, request, data):
        self.render_extension_with_fields(request, 'data', [
            TagData('table', data.get('table', 'ru')),
            TagData('table', data.get('name'))
        ])
