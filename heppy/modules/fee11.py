# -*- coding: utf-8 -*-

from .fee import fee

class fee11(fee):
    opmap = {
        'chkData':      'descend',
        'currency':     'set',
        'class':        'set',
        'fee':          'set',
        'command':      'set',
        'period':       'set',
    }

    def parse_cd(self, response, tag):
        # Real registries (confirmed against Google's registry-sandbox OTE)
        # send <fee:command>create</fee:command> as plain text, with
        # period/fee as siblings of it inside <fee:cd> rather than nested
        # children — hence command_text_fallback=True.
        return self.parse_cd_nested_command(
            response, tag, object_id=False, command_text_fallback=True)

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:command',   {},             data.get('action', 'create'))
        request.add_subtag(ext, 'fee:currency',  {},             data.get('currency', 'USD'))
#        request.add_subtag(ext, 'fee:period',    {'unit':'y'},   data.get('period', 1))
