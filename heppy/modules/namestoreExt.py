from ..Module import Module

class namestoreExt(Module):
    opmap = {
        'nsExtErrData': 'descend',
    }

### RESPONSE parsing

    def parse_msg(self, response, tag):
        if 'code' in tag.attrib:
            response.set('nsExtErr.code', tag.attrib['code'])
        response.set('nsExtErr.msg', tag.text)

### REQUEST rendering

    def render_subProduct(self, request):
        extension = self.render_extension(request, 'namestoreExt')
        request.subfields(extension, {'subProduct': {}}, request.get('namestoreExt'))

