from ..Module import Module
from ..TagData import TagData


class uaepp(Module):
    opmap = {
        'infData':      'descend',
        'license':      'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'uaepp'


    def render_delete(self, request, data):
        self.render_extension_with_fields(request, 'delete', [
            TagData('deleteNS', '', {'confirm': 'yes'})
        ])

    def render_create(self, request, data):
        self.render_extension_with_fields(request, 'create', [
            TagData('license', data.get('license'))
        ])

    def render_update(self, request, data):
        self.render_extension_with_fields(request, 'update', [
            TagData('license', data.get('license'))
        ])

    def render_info(self, request, data):
        return self.render_default(request, data)
