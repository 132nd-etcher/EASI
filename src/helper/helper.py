# coding=utf-8

from src.abstract.abstract_progress import ProgressInterface
from src.dld.download import downloader
from src.helper.abstract import AbstractHelper

HELPER_DIR = r'./helpers'


class BaseHelper(AbstractHelper):
    @property
    def helper_dir(self):
        return HELPER_DIR

    def download(self, progress: ProgressInterface):
        downloader.download_to_file(
            url=self.download_link,
            progress=progress
        )
