# coding=utf-8

import time
import typing

import requests

from src.abstract.abstract_progress import ProgressInterface, DualProgressInterface
from src.low.singleton import Singleton
from src.low.custom_logging import make_logger
from src.low.custom_path import Path, create_temp_file
from src.threadpool import ThreadPool

logger = make_logger(__name__)


class DownloadFile:
    def __init__(self, url: str, outfile: Path or str = None):
        self.__url = url
        self.__header = None
        self.__size = None
        self.__content = None
        self.__success = False
        self.__done = False
        if outfile is None:
            logger.debug('{}: making temp file'.format(url))
            self.__outfile = create_temp_file()
        elif isinstance(outfile, str):
            self.__outfile = Path(outfile)
        elif not isinstance(outfile, Path):
            raise TypeError('expected a Path or a str instance for outfile, got: {}'.format(type(outfile)))

    def wait(self, follow_up: callable = None):
        while not self.done:
            time.sleep(0.1)
        if follow_up:
            follow_up()

    def get_headers(self):
        logger.debug('{}: getting headers'.format(self.url))
        headers_request = requests.head(self.url)
        if not headers_request.status_code == 200:
            logger.error('header request failed: {}'.format(headers_request.reason))
            self.__header = None
        self.__header = headers_request

    def get_content_size(self, _try=1):
        if self.__header is None:
            self.get_headers()
        try:
            self.__size = int(self.__header.headers['Content-Length'])
        except KeyError:
            if _try <= 4:
                self.get_content_size(_try + 1)
            else:
                logger.exception('{}: unable to read size from headers: {}'.format(self.url, self.header.headers))
                self.__size = None
        logger.debug('{}: size: {}'.format(self.url, self.__size))

    def get_content(self):
        logger.info('{}: getting content request'.format(self.url))
        content_request = requests.get(self.url)
        if not content_request.status_code == 200:
            logger.error('content request failed: {}'.format(content_request.reason))
            self.__content = None
        self.__content = content_request

    def download_to_file(self, progress_callback: callable or None):
        self.get_content_size()
        self.get_content()
        if not self.__content:
            self.__success, self.__done = False, True
        logger.info('{}: downloading content to: {}'.format(self.url, self.outfile.abspath()))
        downloaded_size = 0
        with open(self.outfile.abspath(), 'wb') as f:
            logger.debug('{}: downloading content into local file'.format(self.url))
            for data in self.__content.iter_content(chunk_size=Downloader.chunk_size):
                downloaded_size += len(data)
                try:
                    f.write(data)
                except OSError:
                    logger.exception('{}: failed to write data into local file'.format(self.url))
                    self.__success, self.__done = False, True
                if progress_callback is not None and self.size is not None:
                    progress_callback(100 * (downloaded_size / self.size))
        logger.debug('{}: download successful'.format(self.url))
        self.__success, self.__done = True, True
        return self

    @property
    def url(self) -> str:
        return self.__url

    @property
    def size(self):
        return self.__size

    @property
    def outfile(self) -> Path:
        return self.__outfile

    @property
    def header(self) -> requests.models.Response:
        return self.__header

    @header.setter
    def header(self, value: requests.models.Response):
        self.__header = value

    @property
    def content(self) -> requests.models.Response:
        return self.__content

    @content.setter
    def content(self, value: requests.models.Response):
        self.__content = value

    @property
    def success(self) -> bool:
        return self.__success

    @success.setter
    def success(self, value):
        self.__success = value

    @property
    def done(self):
        return self.__done


class DownloadFileList:
    def __init__(self, init_file_list: list = None):
        self.__file_list = init_file_list or []
        self.__d = {file.url: file for file in self.__file_list}
        self.__keys = self.__d.keys()
        self.__items = self.__d.items()
        self.__values = self.__d.values()

    def add_file(self, *, download_file: DownloadFile = None, url: str = None, outfile: Path or str = None):
        if not download_file:
            if not url:
                raise SyntaxError('missing url in method call')
            download_file = DownloadFile(url=url, outfile=outfile)
        self.file_list.append(download_file)
        self.__d[download_file.url] = download_file

    def add_file_from_github(self, user: str, repo: str, file_path: str, branch: str = 'master'):
        self.add_file(url=r'https://raw.githubusercontent.com/{}/{}/{}/{}'.format(
            user, repo, branch, file_path
        ))

    def all_good(self):
        if len(self.file_list) == 0:
            raise ValueError('file list is empty')
        return all([file.success for file in self.file_list])

    def __getitem__(self, key: str or DownloadFile):
        if isinstance(key, DownloadFile):
            key = key.url
        return self.__d[key]

    def __setitem__(self, key, value):
        raise NotImplementedError('cannot set')

    @property
    def file_list(self) -> typing.List[DownloadFile]:
        return self.__file_list

    @property
    def keys(self):
        return self.__keys

    @property
    def values(self):
        return self.__values

    @property
    def items(self):
        return self.__items

    def __iter__(self):
        for x in self.file_list:
            yield x

    def __len__(self):
        return len(self.file_list)


class Downloader(metaclass=Singleton):
    threads_count = 8
    chunk_size = 4096

    def __init__(self):
        self.pool_dl = ThreadPool(_num_threads=Downloader.threads_count, _basename='downloader', _daemon=True)
        self.pool_seq = ThreadPool(_num_threads=1, _basename='downloader watcher', _daemon=True)

    def pause(self):
        self.pool_dl.set_thread_count(0)

    def resume(self):
        self.pool_dl.set_thread_count(Downloader.threads_count)

    def download_to_file(self,
                         url: str,
                         outfile: Path or str = None,
                         progress: ProgressInterface = None) -> DownloadFile:
        download_file = DownloadFile(url, outfile)
        progress.set_text('Downloading {}'.format(url))
        self.pool_dl.queue_task(
            download_file.download_to_file,
            kwargs=dict(progress_callback=progress.set_progress)
        )
        return download_file

    def download_to_file_and_wait(self,
                                  url: str,
                                  outfile: Path or str = None,
                                  progress: ProgressInterface = None) -> DownloadFile:
        dl = self.download_to_file(url, outfile, progress)
        self.pool_seq.queue_task(dl.wait)
        return dl.success

    def __download_multiple_to_file(self,
                                    download_file_list: DownloadFileList,
                                    progress: DualProgressInterface = None):

        total_size = 0
        dl_size = 0
        progress.set_text('Initializing')
        for file in download_file_list:
            progress.set_current_text('{}'.format(file.url))
            file.get_content_size()
            if file.size:
                total_size += file.size
            progress.add_progress(100 / len(download_file_list))

        progress.set_text('Downloading')
        progress.set_progress(0)
        for file in download_file_list:
            progress.set_current_text('{}'.format(file.url))
            file.download_to_file(progress_callback=progress.set_current_progress)
            dl_size += file.size
            progress.set_progress(100 * (dl_size / total_size))

    def download_multiple_to_file(self,
                                  download_file_list: DownloadFileList,
                                  progress: DualProgressInterface = None,
                                  on_completion: callable = None):

        self.pool_seq.queue_task(
            self.__download_multiple_to_file,
            kwargs=dict(download_file_list=download_file_list, progress=progress)
        )
        if on_completion is not None:
            self.pool_seq.queue_task(on_completion)


downloader = Downloader()
