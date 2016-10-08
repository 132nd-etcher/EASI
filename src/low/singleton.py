# coding=utf-8
import abc


class Singleton(abc.ABCMeta):
    """
    When used as metaclass, allow only one instance of a class
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def wipe_instances(mcs):
        """Only for testing purposes"""
        mcs._instances = {}
