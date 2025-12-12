# -*- coding: utf-8 -*-

from fee import fee

class fee21(fee):
    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency',  {}, data.get('currency', 'USD'))
        request.add_subtag(ext, 'fee:command', {'name': data.get('action', 'create')})
