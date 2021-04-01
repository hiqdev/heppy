from ..Module import Module
from ..TagData import TagData

### https://tools.ietf.org/html/rfc7848

class smd(Module):
    opmap = {
        'encodedSignedMark': 'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'smd'

### RESPONSE parsing

### REQUEST rendering
    def render_encoded_signed_mark(self, parent, request, mark):
        return self.render_header(request, parent, 'encodedSignedMark', text=mark)

    def render_signed_mark(self, parent, request, mark):
        return self.render_header(request, parent, 'signedMark', text=mark)
