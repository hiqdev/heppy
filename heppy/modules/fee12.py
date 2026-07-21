# -*- coding: utf-8 -*-

from .fee11 import fee11

class fee12(fee11):
    def parse_cd(self, response, tag):
        return self.parse_cd_nested_command(
            response, tag, object_id=False, lowercase=True)

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency', {}, data.get('currency', 'USD'))
        command = request.add_subtag(ext, 'fee:command', {'name': data.get('action', 'create')})
        request.add_subtag(command, 'fee:period', {'unit': data.get('unit', 'y')}, data.get('period', 1))
