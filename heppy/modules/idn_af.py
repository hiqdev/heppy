# -*- coding: utf-8 -*-
from ..TagData import TagData
from .idn import idn


class idn_af(idn):
    # Afilias legacy IDN namespace; uses 'script' instead of 'table'/'uname'
    opmap = {
        **idn.opmap,
        'script': 'set',
    }

    def __init__(self, xmlns):
        super().__init__(xmlns)
        self.name = 'idn'

### REQUEST rendering

    def render_check(self, request, data):
        self.render_extension_with_fields(request, 'check', [
            TagData('script', data.get('script'))
        ])

    def render_create(self, request, data):
        self.render_extension_with_fields(request, 'create', [
            TagData('script', data.get('script'))
        ])

    def render_update(self, request, data):
        command = self.render_extension(request, 'update')
        chg_element = request.add_subtag(command, self.name + ':chg')
        request.add_subtag(chg_element, self.name + ':script', text=data.get('script'))
