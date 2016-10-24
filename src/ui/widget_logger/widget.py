# coding=utf-8
import logging
import sys

from src.qt import QObject, pyqtSignal, QTextBrowser


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
    def __init__(self, qobj):
        logging.Handler.__init__(self, logging.DEBUG)
        self.qobj = qobj

    def emit(self, record):
        record = self.format(record)
        if record:
            if isinstance(self.qobj, QTextBrowser):
                # self.qobj.insertPlainText('{}\n'.format(record))
                self.qobj.append(record)


class QtLogger:
    msg = pyqtSignal(str, name='msg')

    def __init__(self, parent, qobj):
        self.__logger = logging.getLogger(".".join(['main', parent.__class__.__name__]))
        self.__handler = QtHanlder(qobj)
        self.__handler.setFormatter(logging.Formatter(
            '%(asctime)s: %(levelname)s: %(message)s', "%H:%M:%S"))
        self.__logger.addHandler(self.__handler)
        self.debug = self.__logger.debug
        self.info = self.__logger.info
        self.warn = self.warning = self.__logger.warning
        self.error = self.__logger.error
