from ..Module import Module
from ..TagData import TagData


class neulevel(Module):
    opmap = {
        'extension': 'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'neulevel'

### RESPONSE parsing
    def parse_unspec(self, response, tag):
        pass

    def parse_extension(self, response, tag):
        pass

### REQUEST rendering
    def render_default(self, request, data):
        self.render_extension_with_fields(request, 'extension', [
            TagData('unspec', data.get('neurlevel', 'WhoisType=Natural Publish=Y'))
        ])
