# coding=utf-8

from blinker import Signal


# FIXME: this needs test
class SignalReceiver:
    def __init__(self, parent):
        self.handlers = {}
        self.parent = parent

    def __setitem__(self, signal: Signal, func: callable):
        def handle_sig(sender, **kwargs):
            try:
                func(**kwargs)
            except ValueError:
                if self.parent:
                    raise NotImplementedError('{}: {} has not method: {}'.format(
                        sender, self.parent.__class__.__name__, func.__name__))
                else:
                    raise NotImplementedError('{}: method not found: {}'.format(
                        sender, func.__name__))

        signal.connect(handle_sig)
        self.handlers[signal] = handle_sig

    def __delitem__(self, signal: Signal):
        signal.disconnect(self.handlers[signal])
        del self.handlers[signal]
