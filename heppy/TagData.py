# -*- coding: utf-8 -*-

class TagData:
    def __init__(self, name, value=None, attrs=None):
        self.name = name
        self.value = value
        self.attrs = {} if attrs is None else self.filter_attrs(attrs)

    def filter_attrs(self, attrs):
        return {attr: value for attr, value in attrs.items() if value}
