# coding=utf-8

import binascii
import os
import tempfile

import path
import pefile
# from win32.win32api import GetFileVersionInfo, HIWORD, LOWORD


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

    def normalize(self):
        """
        Transforms a path into an lower case absolute path, with backslashes replaced by slashes
        :param path:
        :return:
        """
        return self.abspath().replace('\\', '/').lower()

    def get_version_info(self):
        """
        Reads the version info string of an executable
        :param path_to_exe: path to the executable file
        :return: version as a String or None
        """
        if not self.exists() or not self.isfile():
            return None
        try:
            pe = pefile.PE(self.abspath())
            if not 'VS_FIXEDFILEINFO' in pe.__dict__:
                return None
                print("ERROR: Oops, %s has no version info. Can't continue." % (self.abspath()))
                return
            if not pe.VS_FIXEDFILEINFO:
                return None
                print("ERROR: VS_FIXEDFILEINFO field not set for %s. Can't continue." % (self.abspath()))
                return
            verinfo = pe.VS_FIXEDFILEINFO
            filever = (verinfo.FileVersionMS >> 16, verinfo.FileVersionMS & 0xFFFF, verinfo.FileVersionLS >> 16, verinfo.FileVersionLS & 0xFFFF)
            prodver = (verinfo.ProductVersionMS >> 16, verinfo.ProductVersionMS & 0xFFFF, verinfo.ProductVersionLS >> 16, verinfo.ProductVersionLS & 0xFFFF)
            return '%d.%d.%d.%d' % filever
        except:
            return None


def create_temp_file(*, suffix=None, prefix=None, create_in_dir=None):
    """
    Creates a temporary path in the user's temp dir
    :param suffix: filename suffix
    :param prefix: filename prefix
    :param create_in_dir: directory in which the file will be created (defaults to temp)
    :return: temporary file path as a string
    """
    os_handle, temp_file = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=create_in_dir)
    os.close(os_handle)
    return Path(temp_file)
