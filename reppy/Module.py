
class Module:
    opmap = {}

    def __init__(self, response):
        self.response = response

    def find(self, tag, name):
        return self.response.find(tag, name)

    def findall(self, tag, name):
        return self.response.findall(tag, name)

    def parse_nothing(self, tag):
        pass

    def parse_set(self, tag):
        self.set(tag.tag.split('}')[1], tag.text)

    def parse_descend(self, tag):
        for child in tag:
            self.response.parse(child)
            
    def set(self, name, value):
        self.response.set(name, value)

    def get(self, name, default):
        self.response.get(name, default)

