# coding=utf-8

from blinker import signal


# noinspection PyPep8Naming
class MetaProperty:
    """Decorator used to define a property of a Meta class

    This is a simple descriptor wrapper to read/write the name of the property to/from the Meta file.
    """

    def __init__(self, func, default, _type):
        self.key = func.__name__
        self.func = func
        self.__doc__ = func.__doc__
        self.default = default
        self.type = _type

    def __get__(self, obj, _):
        if obj is None:
            return self
        if obj.__getitem__(self.key) is None:
            return self.default
        else:
            return obj.__getitem__(self.key)

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            raise TypeError('expected a {}, got: {} (value: {})'.format(str(self.type), type(value), value))
        if obj is None:
            return self
        self.func(obj, value)
        obj.__setitem__(self.key, value)
        signal('{}_value_changed'.format(self.func.__name__)).send('meta', value=value)


# noinspection PyPep8Naming
class MetaPropertyWithDefault:
    """Decorator used to define a property of a Meta class that also has a default value"""

    def __init__(self, default, _type):
        # print('__init__', default)
        self.default = default
        self.type = _type

    def __call__(self, f):
        # print('__call__', f)
        dec = MetaProperty(f, self.default, self.type)
        return dec
