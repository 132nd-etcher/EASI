# coding=utf-8
import logging

from src.qt import QTextBrowser


class QtHandler(logging.Handler):
    def __init__(self, qobj):
        logging.Handler.__init__(self, logging.DEBUG)
        self.qobj = qobj

    def emit(self, record):
        record = self.format(record)
        if record:
            if isinstance(self.qobj, QTextBrowser):
                self.qobj.append(record)


class QtLogger:
    def __init__(self, parent, qobj):
        self.__logger = logging.getLogger(".".join(['main', parent.__class__.__name__]))
        self.__handler = QtHandler(qobj)
        self.__handler.setFormatter(logging.Formatter(
            '%(asctime)s: %(levelname)s: %(message)s', "%H:%M:%S"))
        self.__logger.addHandler(self.__handler)
        self.debug = self.__logger.debug
        self.info = self.__logger.info
        self.warn = self.warning = self.__logger.warning
        self.error = self.__logger.error
