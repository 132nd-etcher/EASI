# coding=utf-8

import binascii
import os
import shutil
import tempfile
import win32api
import pywintypes

import path
from humanize import filesize


class Win32FileInfo:
    def __init__(self, path: str or Path):
        self.__path = str(Path(path).abspath())
        self.__props = None
        self.__read_props()

    @property
    def comments(self):
        return self.__props.get('Comments')

    @property
    def internal_name(self):
        return self.__props.get('InternalName')

    @property
    def product_name(self):
        return self.__props.get('ProductName')

    @property
    def company_name(self):
        return self.__props.get('CompanyName')

    @property
    def copyright(self):
        return self.__props.get('LegalCopyright')

    @property
    def product_version(self):
        return self.__props.get('ProductVersion')

    @property
    def file_description(self):
        return self.__props.get('FileDescription')

    @property
    def trademark(self):
        return self.__props.get('LegalTrademarks')

    @property
    def private_build(self):
        return self.__props.get('PrivateBuild')

    @property
    def file_version(self):
        return self.__props.get('FileVersion')

    @property
    def fixed_version(self):
        return self.__props.get('fixed_version')

    @property
    def original_filename(self):
        return self.__props.get('OriginalFilename')

    @property
    def special_build(self):
        return self.__props.get('SpecialBuild')

    def __read_props(self):
        prop_names = ('Comments', 'InternalName', 'ProductName',
                      'CompanyName', 'LegalCopyright', 'ProductVersion',
                      'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                      'FileVersion', 'OriginalFilename', 'SpecialBuild')
        self.__props = {}
        try:
            fixed_info = win32api.GetFileVersionInfo(self.__path, '\\')
            self.__props['fixed_version'] = "%d.%d.%d.%d" % (fixed_info['FileVersionMS'] / 65536,
                                                             fixed_info['FileVersionMS'] % 65536,
                                                             fixed_info['FileVersionLS'] / 65536,
                                                             fixed_info['FileVersionLS'] % 65536)
            lang, codepage = win32api.GetFileVersionInfo(self.__path, '\\VarFileInfo\\Translation')[0]
            for name in prop_names:
                try:
                    self.__props[name] = str(win32api.GetFileVersionInfo(
                        self.__path,
                        u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, name)
                    )).strip(' ')
                    if self.__props[name] == 'None':
                        self.__props[name] = None
                except:
                    raise
        except getattr(pywintypes, 'error') as e:
            if e.winerror == 1812:
                raise ValueError('Win32FileInfo: {}: {}'.format(self.__path, e.strerror.lower()))


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

    def human_size(self) -> str:
        return filesize.naturalsize(self.getsize(), gnu=True)

    def normalize(self) -> str:
        return self.abspath().replace('\\', '/').lower()

    def get_win32_file_info(self) -> Win32FileInfo:
        if not self.exists():
            raise FileNotFoundError(self.abspath())
        elif not self.isfile():
            raise TypeError(self.abspath())
        return Win32FileInfo(self)

    def get_version_info_pefile(self) -> str:
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
        file_ver = (verinfo.FileVersionMS >> 16, verinfo.FileVersionMS & 0xFFFF, verinfo.FileVersionLS >> 16,
                    verinfo.FileVersionLS & 0xFFFF)
        # prod_ver = (verinfo.ProductVersionMS >> 16, verinfo.ProductVersionMS & 0xFFFF,
        # verinfo.ProductVersionLS >> 16, verinfo.ProductVersionLS & 0xFFFF)
        return '%d.%d.%d.%d' % file_ver

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
