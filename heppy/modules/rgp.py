from ..Module import Module
from ..TagData import TagData


class rgp(Module):
    opmap = {
        'infData':      'descend',
    }

    def parse_rgpStatus(self, response, tag):
        status = tag.attrib['s']
        response.set(status, tag.text)

    def render_default(self, request, data):
        ext = self.render_extension(request, 'update')
        request.add_subtag(ext, 'rgp:restore', { 'op': 'request'})

