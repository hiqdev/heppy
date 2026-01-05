# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData


class sync(Module):

### RESPONSE parsing

    def parse_sync(self, response, tag):
        response.put_extension_block(response, 'namestoreExt', tag, {
            'subProduct': [],
        })

### REQUEST rendering

    def render_default(self, request, data):
        self.render_extension_with_fields(request, 'update', [
            TagData('expMonthDay', data.get('expMonthDay'))
        ])


