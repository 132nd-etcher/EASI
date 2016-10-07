# coding=utf-8

import time

from requests import head, get
from requests.exceptions import InvalidURL, MissingSchema

from src.abstract.abstract_progress import ProgressInterface
from src.low.custom_logging import make_logger
from src.low.custom_path import Path, create_temp_file
from src.threadpool import ThreadPool

logger = make_logger(__name__)


class DownloadError(Exception):
    pass


class FileDownload:
    def __init__(self, url: str, local_file: Path or str = None):
        if local_file is None:
            local_file = create_temp_file()
        else:
            local_file = self.normalize_local_file(local_file)
        self.url = url
        self.err = None
        self.done = False
        self.success = False
        self.local_file = local_file
        self.header = None
        self.size = None

    @staticmethod
    def normalize_local_file(local_file):
        if isinstance(local_file, str):
            return Path(local_file)
        elif isinstance(local_file, Path):
            return local_file
        elif local_file is None:
            return Path(create_temp_file())
        else:
            raise TypeError('expected str or Path, got: {}'.format(type(local_file)))

    def wait(self):
        while not self.done:
            time.sleep(0.1)

    def queue_callback(self, callback: callable):
        self.wait()
        callback(self)

    def __fail(self, err: str):
        self.err = err
        logger.error('{}: download failed: {}'.format(self.url, err))
        self.success = False
        self.done = True

    def __make_request(self, method):
        try:
            req = method(self.url, allow_redirects=True)
        except InvalidURL:
            self.__fail('invalid url')
        except MissingSchema:
            self.__fail('missing schema')
        except Exception as e:
            self.__fail(e.__str__())
        else:
            # if req.is_redirect or req.is_permanent_redirect:
            #     self.url = req.
            # if 300 <= req.status_code < 400:
            #     logger.info('redirection, getting location')
            #     self.url = req.
            #     return self.__ma
            if req.status_code != 200:
                self.__fail('{}: request failed: {}: {}'.format(self.url, req.status_code, req.reason))
            return req

        # invalid syntax (<string>, line 1)
        # 'https://github-cloud.s3.amazonaws.com/releases/69669314/82ed146a-8b2a-11e6-9f69-d3b8d9c0da86.exe?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAISTNZFOVBIJMK3TQ%2F20161005%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20161005T170455Z&X-Amz-Expires=300&X-Amz-Signature=e07603c53eda7c30138ea9219669cd9953c2095f0edba7d230dde4fb9cb1eb57&X-Amz-SignedHeaders=host&actor_id=0&response-content-disposition=attachment%3B%20filename%3DEASI_setup_0.0.11.10762.exe&response-content-type=application%2Foctet-stream'

    def get_size(self, _try=1):
        header = self.__make_request(head)
        if header:
            try:
                self.size = int(header.headers['Content-Length'])
                return self.size
            except KeyError:
                if _try >= 4:
                    logger.warning('{}: failed to get size value from headers'.format(self.url))
                    return None
                return self.get_size(_try + 1)

    def download(self, progress_callback: callable = None):
        if self.size is None:
            self.size = self.get_size()
        dl = 0
        content = self.__make_request(get)
        if content:
            try:
                with open(self.local_file.abspath(), 'wb') as f:
                    for data in content.iter_content(chunk_size=Downloader.chunk_size):
                        dl += len(data)
                        f.write(data)
                        if self.size is not None and progress_callback is not None:
                            progress_callback(100 * (dl / self.size))
            except OSError:
                self.__fail('{}: failed to write on local file: {}'.format(self.url, self.local_file.abspath()))
            self.success, self.done = True, True


class BulkFileDownload:
    def __init__(self, fdl_list: list = None):
        if fdl_list is not None:
            if not isinstance(fdl_list, list):
                raise TypeError('expected a list, got: {}'.format(type(fdl_list)))
            for x in fdl_list:
                if isinstance(x, FileDownload):
                    pass
                else:
                    raise TypeError('(in file_list) expected a FileDownload or a tuple/list '
                                    'of (url, local_file), got: {}'.format(type(x)))
        else:
            fdl_list = list()
        self.fdl_list = fdl_list

    def queue_callback(self, callback: callable):
        if callback:
            callback(self)

    def wait(self):
        while not self.done:
            time.sleep(0.1)

    def add_file(self, fdl: FileDownload):
        self.fdl_list.append(fdl)

    @property
    def done(self):
        return all([f.done for f in self.fdl_list])

    @property
    def success(self):
        return all([f.success for f in self.fdl_list])

    @property
    def total_size(self):
        return sum([fdl.size for fdl in self.fdl_list])


class Downloader:
    chunk_size = 4096

    def __init__(self):
        self.watchdog = ThreadPool(1, 'downloader', True)
        self.pool = ThreadPool(8, 'download_pool', True)

    @staticmethod
    def download_fdl(fdl: FileDownload, progress_callback: callable = None, raise_err: bool = False):
        """
        *BLOCKING*

        :param progress_callback: callback used to update progress (if any)
        :param fdl: instance of FileDownload to download
        :param raise_err: whether or not to raise Exceptions that happened during download
        :return: FileDownload object
        """
        fdl.download(progress_callback=progress_callback)
        if raise_err and fdl.err:
            raise DownloadError(fdl.err)
        return fdl

    def __download(self,
                   fdl,
                   progress: ProgressInterface = None,
                   raise_err: bool = True) -> FileDownload:
        if progress:
            progress.set_text('Downloading:\n{}'.format(fdl.url))
            progress.set_progress(0)
        kwargs = dict(fdl=fdl, raise_err=raise_err)
        if progress:
            kwargs['progress_callback'] = progress.set_progress
        self.pool.queue_task(self.download_fdl, kwargs=kwargs)
        fdl.wait()

    def download(self,
                 url,
                 local_file: str or Path = None,
                 progress: ProgressInterface = None,
                 callback: callable = None,
                 raise_err: bool = True,
                 size: int = None) -> FileDownload:
        """
        Downloads the content of a URL into a local file

        :param url: str
        :param local_file: str or Path to local file
        :param progress: instance of ProgressInterface (has "set_progress", "set_text"
        :param callback: will be called after download with FileDownload obj as first arg
        :param raise_err: whether or not to raise Exceptions that happened during download
        :return: FileDownload object
        """
        fdl = FileDownload(url, local_file)
        if size:
            fdl.size = size
        self.watchdog.queue_task(self.__download, kwargs=dict(fdl=fdl, progress=progress, raise_err=raise_err))
        if callback:
            self.watchdog.queue_task(fdl.queue_callback, [callback])
        return fdl

    def bulk_download(self,
                      fdl_list,
                      progress: ProgressInterface = None,
                      callback: callable = None,
                      raise_err: bool = True):

        total_size = 0

        def __gather_metadata():
            nonlocal total_size
            if progress:
                progress.set_text('Gathering metadata...')
            count = 0
            for fdl in fdl_list:
                assert isinstance(fdl, FileDownload)
                fdl.get_size()
                total_size += fdl.size
                if raise_err and fdl.err:
                    raise DownloadError(fdl.err)
                count += 1
                if progress:
                    progress.set_progress((count / len(fdl_list)) * 100)
            print('total size', total_size)

        def __download_content():

            current = 0
            fdl = None

            def __set_composite_progress(value):
                if fdl is None:
                    return
                partial_size = (value / 100) * fdl.size
                progress.set_current_progress(value)
                progress.set_progress(((current + partial_size) / total_size) * 100)

            if progress:
                progress.set_text('Downloading files...')
                progress.set_progress(0)
                progress.set_current_enabled(True)
            for fdl in fdl_list:
                if progress:
                    progress.set_current_text(fdl.url)
                assert isinstance(fdl, FileDownload)
                kwargs = dict(fdl=fdl, raise_err=raise_err)
                if progress:
                    kwargs['progress_callback'] = __set_composite_progress
                self.pool.queue_task(downloader.download_fdl, kwargs=kwargs)
                if raise_err and fdl.err:
                    raise DownloadError(fdl.err)
                fdl.wait()
                current += fdl.size

        bdl = BulkFileDownload(fdl_list)
        self.watchdog.queue_task(__gather_metadata)
        self.watchdog.queue_task(__download_content)
        if callback:
            self.watchdog.queue_task(bdl.queue_callback, [callback])
        return bdl


downloader = Downloader()
