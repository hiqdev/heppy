from Module import Module

class oxrs(Module):
    def parse_xcp(self, tag):
        self.set('result.reason', tag.text)

