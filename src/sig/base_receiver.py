# coding=utf-8

from blinker import Signal


class SignalReceiver:
    def __init__(self, parent):
        self.handlers = {}
        self.parent = parent

    def __setitem__(self, signal: Signal, func: callable):
        def handle_sig(sender, **kwargs):
            try:
                func(**kwargs)
            except ValueError:
                raise NotImplementedError(
                    '{}: {} has not method: {})'.format(sender, self.parent.__class__.__name__, kwargs))

        signal.connect(handle_sig)
        self.handlers[signal] = handle_sig

    def __delitem__(self, signal: Signal):
        signal.disconnect(self.handlers[signal])
        del self.handlers[signal]
