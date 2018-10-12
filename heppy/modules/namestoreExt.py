from ..Module import Module
from ..TagData import TagData


class namestoreExt(Module):

### RESPONSE parsing

    def parse_namestoreExt(self, response, tag):
        response.put_extension_block(response, 'namestoreExt', tag, {
            'subProduct': [],
        })

    def parse_nsExtErrData(self, response, tag):
        response.put_extension_block(response, 'namestoreExt:nsExtErrData', tag, {
            'msg': ['code'],
        })

### REQUEST rendering

    def render_default(self, request, data):
        self.render_extension_with_fields(request, 'namestoreExt', [
            TagData('subProduct', data.get('subProduct'))
        ])

