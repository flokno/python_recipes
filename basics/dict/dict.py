from collections import OrderedDict


class ClassDict(OrderedDict):
    """Dictionary that supports .attribute access."""

    def __init__(self, *args, **kwargs):
        super(ClassDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class AttributeDict(OrderedDict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value
