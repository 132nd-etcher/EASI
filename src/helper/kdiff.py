# coding=utf-8

from src.helper.helper import BaseHelper
from src.sig import sig_long_op_dialog


class KdiffHelper(BaseHelper):
    def __init__(self):
        BaseHelper.__init__(self)

    @property
    def executable(self):
        return ''

    @property
    def name(self):
        return 'kdiff3'

    @property
    def download_link(self):
        return r'https://codeload.github.com/132nd-etcher/kdiff3/zip/master'
