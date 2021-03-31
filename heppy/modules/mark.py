from ..Module import Module
from ..TagData import TagData

### https://tools.ietf.org/html/rfc7848

class mark(Module):
    opmap = {
        'mark': 'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'mark'

### RESPONSE parsing

### REQUEST rendering
    def render_mark(self, parent, request, mark):
        return self.render_header(request, parent, 'mark', text=mark)

