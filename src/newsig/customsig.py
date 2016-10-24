# coding=utf-8

import types

from blinker import signal


class CustomSig(type):
    """
    Meant to be used as a metaclass only !

    Defines a custom signal by replacing all methods that do not start with "_"

    """
    def __new__(mcs, name, bases, attrs):

        for attr_name, attr_value in attrs.items():
            if attr_name.startswith('_'):
                continue
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = mcs.send_sig_decorator(attr_value)
        return super(CustomSig, mcs).__new__(mcs, name, bases, attrs)

    @classmethod
    def send_sig_decorator(mcs, func):

        def wrapper(instance, *args, **kwargs):
            func(instance, *args, **kwargs)
            print(instance, args, kwargs)
            signal(instance.__class__.__name__).send(instance, op=func.__name__, args=args,  **kwargs)

        return wrapper
