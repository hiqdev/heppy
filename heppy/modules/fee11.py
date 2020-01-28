from fee import fee

class fee11(fee):
    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency',  {},             data.get('currency'))
        request.add_subtag(ext, 'fee:command',   {},             data.get('action'))
        request.add_subtag(ext, 'fee:period',    {'unit':'y'},   data.get('period'))
