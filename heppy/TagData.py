# -*- coding: utf-8 -*-

class TagData:
    def __init__(self, name, value=None, attrs={}):
        self.name = name
        self.value = value
        self.attrs = self.filter_attrs(attrs)

    def filter_attrs(self, attrs):
        return {attr: value for attr, value in attrs.items() if value}
