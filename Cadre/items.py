# -*- coding: utf-8 -*-
"""
Created by suun on 5/5/2018
"""


class Field(dict):
    """Container of field"""


class Item(object):

    def __init__(self, *args, **kwargs):
        self.fields = {}
        for k in dir(self):
            v = getattr(self, k)
            if isinstance(v, Field):
                self.fields[k] = v
        self._values = {}
        if args or kwargs:
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __getitem__(self, item):
        return self._values[item]

    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
        else:
            raise KeyError("%s does not support field: %s" % (self.__class__.__name__, key))

    def __delitem__(self, key):
        del self._values[key]

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def __getattr__(self, item):
        return getattr(self._values, item)

    # def keys(self):
    #     return self._values.keys()
    #
    # def values(self):
    #     return self._values.items()
    #
    # def items(self):
    #     return self._values.items()
    #
    def __repr__(self):
        return repr(self._values)

    def __str__(self):
        return str(self._values)


class DefaultItem(Item):
    url = Field()
    content = Field()
