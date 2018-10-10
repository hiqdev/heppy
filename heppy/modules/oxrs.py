from ..Module import Module


class oxrs(Module):
    def parse_xcp(self, response, tag):
        response.set('result_reason', tag.text)

