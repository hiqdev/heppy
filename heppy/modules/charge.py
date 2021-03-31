from ..Module import Module
from ..TagData import TagData
from pprint import pprint

class charge(Module):
    opmap = {
        'creData':  'descend',
        'checkData': 'descend',
        'renData': 'descend',
        'trnData': 'descend',
        'set': 'descend',
        'name': 'set',
        'type': 'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'charge'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

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

    def render_restore(self, request, data):
        return self.render_agreement(request, data, 'update')

    def render_agreement(self, request, data, action='create'):
        category_name = {}
        if data.get('category_name'):
            category_name = {'name': data.get('category_name')}
        if data.get('action'):
            action = data.get('action')
        command = {"command": action}
        if action == 'update':
            command = {"command": "update", "name": "restore"}
        return self.render_command_with_fields(request, 'charge:set' [
            TagData('category', data.get('category', 'premium'), category_name),
            TagData('type', data.get('type', 'price')),
            TagData('amount', data.get('amount'), command)
        ])

