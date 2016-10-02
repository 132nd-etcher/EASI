# coding=utf-8


from blinker import Signal


class CustomSignal(Signal):
    def __init__(self):
        Signal.__init__(self)

    def send(self, *args, **kwargs):
        if args:
            super(CustomSignal, self).send(self.__class__.__name__, args=args, **kwargs)
        else:
            super(CustomSignal, self).send(self.__class__.__name__, **kwargs)
