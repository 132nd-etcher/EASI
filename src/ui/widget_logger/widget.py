# coding=utf-8
import logging
import sys
from src.qt import QObject, pyqtSignal


class XStream(QObject):
    _stdout = None
    _stderr = None
    messageWritten = pyqtSignal(str, name='msg')

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


class QtHanlder(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self, logging.DEBUG)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('{}\n'.format(record))


class QtLogger:
    msg = pyqtSignal(str, name='msg')

    def __init__(self, qobj):
        self.__logger = logging.getLogger('QtLogger')
        self.qob = qobj

    def __enter__(self):
        return self.__logger



    @property
    def logger(self):
        return self.__logger

    def set_output(self, q_widget):
        self.__logger.addHandler()