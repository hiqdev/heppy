# -*- coding: utf-8 -*-

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

    # render_info/render_create/render_renew/render_transfer: no override
    # needed, fee.py's versions (inherited via fee09) already match — these
    # used to be duplicated here verbatim.
