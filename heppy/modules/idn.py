from ..Module import Module
from ..TagData import TagData


class idn(Module):

### RESPONSE parsing

    def parse_infData(self, response, tag):
        response.put_extension_block(response, 'idn:info', tag, {
            'script': [],
        })

### REQUEST rendering

    def render_check(self, request, data):
        self.render_extension_with_fields(request, 'check', [
            TagData('script', data.get('script'))
        ])

    def render_create(self, request, data):
        self.render_extension_with_fields(request, 'create', [
            TagData('script', data.get('script'))
        ])

    def render_update(self, request, data):
        command = self.render_extension(request, 'update')
        chg_element = request.add_subtag(command, 'idn:chg')
        request.add_subtag(chg_element, 'idn:script', text=data.get('script'))
