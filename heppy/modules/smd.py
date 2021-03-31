from ..Module import Module
from ..TagData import TagData
from pprint import pprint

### https://tools.ietf.org/html/rfc8334

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
        return self.render_header(request, parent, 'encodedSignedMark', text=mark);

