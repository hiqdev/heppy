from ..Module import Module
from ..TagData import TagData

### https://tools.ietf.org/html/rfc7848

class launch(Module):
    opmap = {
        'encodedSignedMark': 'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'smd'

### RESPONSE parsing

### REQUEST rendering
    def render_encodedSignedMark(self, parent, request, mark):
        return self.render_header(request, parent, 'encodedSignedMark', mark);
