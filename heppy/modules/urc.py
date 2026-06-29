# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData


class urc(Module):
    opmap = {
        'registrant':   'set',
        'postalInfo':   'descend',
        'addr':         'descend',
        'name':         'set',
        'org':          'set',
        'street':       'set',
        'city':         'set',
        'pc':           'set',
        'sp':           'set',
        'cc':           'set',
        'email':        'set',
        'voice':        'set',
        'fax':          'set',
        'emailAlt':     'set',
        'mobile':       'set',
        'security':     'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'urc'

### RESPONSE parsing

### REQUEST rendering
    def render_default(self, request, data):
        command = self.render_command_with_fields(request, 'registrant', [])
        self.render_postal_info(request, data, command)
        self.render_contact_info(request, data, command)

    def render_create(self, request, data):
        return self.render_default(request, data)

    def render_update(self, request, data):
        return self.render_default(request, data)

    def render_delete(self, request, data):
        pass

    def render_postal_info(self, request, data, parent):
        attrs = {'type': data.get('type', 'int')}
        postal_info = request.add_subtag(parent, 'contact:postalInfo', attrs)
        for key in ['name', 'org']:
            request.add_subtag(postal_info, 'urc:'+key, text=data.get(key))

    def render_addr(self, request, parent, data):
        addr = request.add_subtag(parent, 'urc:addr')
        for key in ['street', 'city', 'sp', 'pc', 'cc']:
            if key in data:
                request.add_subtag(addr, 'urc:'+key, text=data.get(key))

    def render_contact_info(self, request, data, parent):
        for key in ['voice', 'email', 'emailAlt', 'mobile']:
            request.add_subtag(parent, 'urc:'+key, text=data.get(key))

