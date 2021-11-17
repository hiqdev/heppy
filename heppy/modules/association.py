from ..Module import Module
from ..TagData import TagData


class association(Module):
    opmap = {
        'infData':      'descend',
        'contact':      'descend',
        'id':           'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'association'

### RESPONSE parsing

### REQUEST rendering

    def render_create(self, request, data):
        ext = self.render_extension(request, 'create')
        contact = request.add_subtag(ext, 'association:contact', {'type': 'membership'})
        request.add_subtag(contact, 'association:id', {}, data.get('token'))

    def render_update(self, request, data):
        ext = self.render_extension(request, 'update')
        chg = request.add_subtag(ext, 'association:add')
        contact = request.add_subtag(chg, 'association:contact', {'type': 'membership'})
        request.add_subtag(contact, 'association:id', {}, data.get('token'))


