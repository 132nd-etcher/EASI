# coding=utf-8
import abc

from src.low import constants
from src.low.custom_logging import make_logger


class Singleton(abc.ABCMeta):
    """
    When used as metaclass, allow only one instance of a class
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls.__name__ not in cls._instances:
            cls._instances[cls.__name__] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls.__name__]

    # noinspection PyMethodParameters
    @classmethod
    def wipe_instances(cls, cls_to_remove):
        """Only for testing purposes"""
        for instance in cls._instances:
            if cls_to_remove == instance:
                if constants.TESTING:
                    make_logger(__name__).debug('wiping "{}" instances'.format(instance))
                del cls._instances[instance]
                return
