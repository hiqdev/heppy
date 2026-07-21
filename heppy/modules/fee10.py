# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData
from .fee09 import fee09

class fee10(fee09):
    opmap = {
        'chkData':      'descend',
        'currency':     'set',
        'period':       'set',
        'fee':          'set',
    }

    def parse_cd(self, response, tag):
        return self.parse_cd_nested_command(
            response, tag, object_id=True, lowercase=True, always_store=True)

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency', {}, data.get('currency', 'USD'))
        command = request.add_subtag(ext, 'fee:command', {'name': data.get('action', 'create')})
        request.add_subtag(command, 'fee:period', {'unit': data.get('unit', 'y')}, data.get('period', 1))

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
