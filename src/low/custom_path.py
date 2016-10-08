# coding=utf-8

import shutil
import binascii
import os
import tempfile

import path
import pefile
from humanize import filesize


# noinspection PyAbstractClass
class Path(path.Path):
    def crc32(self):

        if not self.isfile():
            raise TypeError('cannot compute crc32, not a file: {}'.format(self.abspath()))
        else:
            try:
                with open(self.abspath(), 'rb') as buf:
                    buf = "%08X" % (binascii.crc32(buf.read()) & 0xFFFFFFFF)
                    return buf
            except:
                raise RuntimeError('failed to compute crc32 for: {}'.format(self.abspath()))

    def human_size(self):
        return filesize.naturalsize(self.getsize(), gnu=True)

    def normalize(self):
        return self.abspath().replace('\\', '/').lower()

    def get_version_info(self):
        if not self.exists():
            raise FileNotFoundError(self.abspath())
        if not self.isfile():
            raise TypeError('not a file: {}'.format(self.abspath()))
        try:
            pe = pefile.PE(self.abspath())
        except pefile.PEFormatError:
            raise ValueError('file has no version: {}'.format(self.abspath()))
        if 'VS_FIXEDFILEINFO' not in pe.__dict__ or not pe.VS_FIXEDFILEINFO:
            raise ValueError('file has no version: {}'.format(self.abspath()))
        verinfo = pe.VS_FIXEDFILEINFO
        filever = (verinfo.FileVersionMS >> 16, verinfo.FileVersionMS & 0xFFFF, verinfo.FileVersionLS >> 16,
                   verinfo.FileVersionLS & 0xFFFF)
        # prodver = (verinfo.ProductVersionMS >> 16, verinfo.ProductVersionMS & 0xFFFF,
        # verinfo.ProductVersionLS >> 16, verinfo.ProductVersionLS & 0xFFFF)
        return '%d.%d.%d.%d' % filever

    def abspath(self):
        return path.Path.abspath(self)

    def exists(self):
        return path.Path.exists(self)

    def get_size(self):
        return path.Path.getsize(self)

    def remove(self):
        return path.Path.remove(self)

    def text(self, encoding=None, errors='strict'):
        return path.Path.text(self, encoding, errors)

    def write_text(self, text, encoding=None, errors='strict',
                   linesep=os.linesep, append=False):
        return path.Path.write_text(self, text, encoding, errors, linesep, append)

    def rmtree(self, must_exist=True):
        if not self.isdir():
            raise TypeError('not a directory: {}'.format(self.abspath()))
        if must_exist and not self.exists():
            raise ValueError('directory does not exist: {}'.format(self.abspath()))
        shutil.rmtree(self.abspath())


def create_temp_file(*, suffix=None, prefix=None, create_in_dir=None) -> Path:
    """
    Creates a temporary path in the user's temp dir
    :param suffix: filename suffix
    :param prefix: filename prefix
    :param create_in_dir: directory in which the file will be created (defaults to temp)
    :return: temporary file path as a string
    """
    if create_in_dir is None:
        create_in_dir = tempfile.gettempdir()
    os_handle, temp_file = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=create_in_dir)
    os.close(os_handle)
    return Path(temp_file)


def create_temp_dir(*, suffix=None, prefix=None, create_in_dir=None) -> Path:
    """
    Creates a temporary path in the user's temp dir
    :param suffix: filename suffix
    :param prefix: filename prefix
    :param create_in_dir: directory in which the file will be created (defaults to temp)
    :return: temporary file path as a string
    """
    if create_in_dir is None:
        create_in_dir = tempfile.gettempdir()
    temp_dir = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=create_in_dir)
    return Path(temp_dir)
