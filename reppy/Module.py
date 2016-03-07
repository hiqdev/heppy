
class Module:
    opmap = {}

    def __init__(self, xmlns):
        self.name   = self.__class__.__name__
        self.xmlns  = xmlns

### RESPONSE parsing

    def parse_nothing(self, response, tag):
        pass

    def parse_set(self, response, tag):
        response.set(tag.tag.split('}')[1], tag.text)

    def parse_descend(self, response, tag):
        for child in tag:
            response.parse(child)

### REQUEST rendering

    def render_epp(self, request):
        if request.epp is None:
            request.epp = request.element('epp', {'xmlns': request.get_module('epp').xmlns})
        return request.epp

    def render_clTRID(self, request):
        clTRID = request.get('clTRID', 'AA-00')
        if clTRID != 'NONE' and request.command is not None:
            request.sub(request.command, 'clTRID', {}, clTRID)

    def render_command(self, request, command):
        if request.command is None:
            epp = self.render_epp(request)
            request.command = request.sub(epp, 'command')
        return request.sub(request.command, command)

    def render_header(self, request, source, action):
        return request.sub(source, self.name + ':' + action, {'xmlns:' + self.name: self.xmlns})

    def render_action(self, request, action):
        command = self.render_command(request, action)
        return self.render_header(request, command, action)

    def render_named_command(self, request, command, fields = {'name': {}}):
        action = self.render_action(request, command)
        self.render_fields(request, action, fields)

    def render_extension(self, request):
        if request.extension is None:
            request.extension = request.sub(request.command, 'extension')
        return request.extension

    def render_the_extension(self, request, action):
        extension = self.render_extension(request)
        return self.render_header(request, extension, action)

    def render_named_extension(self, request, action, fields):
        extension = self.render_the_extension(request, action)
        self.render_fields(extension, extension, fields)

