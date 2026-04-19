# -*- coding: utf-8 -*-

from ..Module import Module

class idnLang(Module):

### REQUEST rendering

    def render_default(self, request, data):
        self.render_extension(request, 'tag', text=data.get('language'))
