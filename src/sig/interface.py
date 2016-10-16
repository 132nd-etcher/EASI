# coding=utf-8
from src.sig.base_custom_signal import CustomSignal


def interfaced_method(func):
    def _wrapper(self, *args, **kwargs):
        return self.send('{}'.format(func.__name__), *args, **kwargs)
        # try:
        #     return self.send('{}'.format(func.__name__), *args, **kwargs)
        # except AttributeError:
        #     raise AttributeError('unknown function in MainInterface: {}'.format(func.__name__))

    return _wrapper


class InterfacedSignal(CustomSignal):
    def __init__(self):
        CustomSignal.__init__(self)

    def send(self, op: str, *args, **kwargs):
        super(InterfacedSignal, self).send(op=op, *args, **kwargs)
