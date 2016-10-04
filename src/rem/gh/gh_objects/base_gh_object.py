# coding=utf-8

# from requests.models import Response


class BaseGHObject:
    def __init__(self, json):
        self._json = json

    @property
    def json(self) -> dict:
        return self._json

    @property
    def header(self):
        return self.json['header']

    def get_all(self):
        ret = []
        for k in self.__class__.__dict__:
            if k.startswith('__'):
                continue
            if callable(getattr(self, k)):
                ret.append((k, getattr(self, k)().get_all()))
            else:
                ret.append((k, getattr(self, k)))
        return ret
        # return [getattr(self, k)  if not k.startswith('__')]


# noinspection PyPep8Naming
class json_property:
    """Wraps around properties to extract JSON key"""

    def __init__(self, func):
        self.key = func.__name__
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, obj, _):
        if obj is None:
            return self
        if not hasattr(obj, 'json'):
            raise NotImplementedError('this object does not support JSON properties')
        return obj.json.get(self.key, None)
