# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData

class charge(Module):
    opmap = {
        'creData':  'descend',
        'chkData':  'descend',
        'renData':  'descend',
        'trnData':  'descend',
        'infData':  'descend',
        'upData':   'descend',
        'agreement':'descend',
        'cd':       'descend',
        'set':      'descend',
        'name':     'set',
        'type':     'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'charge'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

    def parse_category(self, response, tag):
        response.set('category', tag.text.lower())
        response.set('category_name', tag.attrib['name'])

    def parse_amount(self, response, tag):
        response.set(tag.attrib['command'], tag.text.lower())

### REQUEST rendering
    def render_create(self, request, data):
        return self.render_agreement(request, data)

    def render_renew(self, request, data):
        return self.render_agreement(request, data, 'renew')

    def render_transfer(self, request, data):
        return self.render_agreement(request, data, 'transfer')

    def render_update(self, request, data):
        return self.render_restore(request, data)

    def render_restore(self, request, data):
        return self.render_agreement(request, data, 'update')

    def render_default(self, request, data):
        return self.render_agreement(request, data, 'create')

    def render_agreement(self, request, data, action='create'):
        category_name = {}
        if data.get('category_name'):
            category_name = {'name': data.get('category_name')}
        if data.get('action'):
            action = data.get('action')
        command = {"command": action}
        if action == 'update':
            command = {"command": "update", "name": "restore"}

        ext = self.render_extension(request, 'agreement');
        tag = request.add_subtag(ext, 'charge:set')
        request.add_subtag(tag, 'charge:category', category_name, data.get('category', 'premium'))
        request.add_subtag(tag, 'charge:type', {}, data.get('type', 'price'))
        request.add_subtag(tag, 'charge:amount', command, data.get('amount'))
        return request

