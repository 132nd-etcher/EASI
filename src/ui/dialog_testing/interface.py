# coding=utf-8

import abc


class TestingDialogInterface:
    @abc.abstractmethod
    def show(self):
        """Shows this dialog"""
