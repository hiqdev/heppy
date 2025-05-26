# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData

class finance(Module):
    opmap = {
        'infData':  'descend',
        'balance':  'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'finance'

### RESPONSE parsing

### REQUEST rendering

    def render_info(self, request, data):
        return self.render_default(request, data)

    def render_default(self, request, data):
        command = self.render_command_with_fields(request, 'info', [
        ])
