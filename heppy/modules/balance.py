# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData


class balance(Module):
    opmap = {
        'infData':      'descend',
        'contract':     'set',
        'contractUntil':'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'balance'

    def parse_status(self, response, tag):
        status = tag.attrib['s']
        response.set('status', status)

    def parse_balance(self, response, tag):
        date = tag.attrib['bdate']
        response.set('date', date)
        response.set('balance', tag.text)

    def render_default(self, request, data):
        command = self.render_command_with_fields(request, 'info', [
            TagData('contract', data.get('contract'))
        ])

    def render_info(self, request, data):
        return self.render_default(request, data)
