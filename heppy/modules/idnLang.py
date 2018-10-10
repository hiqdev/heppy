from ..Module import Module


class idnLang(Module):
    opmap = {
        'nsExtErrData': 'descend',
    }

### RESPONSE parsing

    def parse_msg(self, response, tag):
        if 'code' in tag.attrib:
            response.set('nsExtErr.code', tag.attrib['code'])
        response.set('nsExtErr.msg', tag.text)

### REQUEST rendering

    def render_default(self, request, data):
        self.render_extension(request, 'tag', text=data.get('language'))
