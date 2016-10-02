# coding=utf-8
import requests

from src.low.custom_logging import make_logger
from src.low.version import Version

logger = make_logger(__name__)


class GHLatest:
    def __init__(self, user: str, repo: str):
        url = 'https://api.github.com/repos/{}/{}/releases/latest'.format(user, repo)
        req = requests.get(url)
        if req is None or not req.ok:
            raise ConnectionError('request failed')
        else:
            self.json = req.json()

    def print_all(self):
        for k in self.json:
            print(k, ':', self.json[k])

    @property
    def name(self):
        return self.json['name']

    def date(self):
        return self.json['published_at']

    @property
    def pre_release(self):
        return self.json['prerelease']

    @property
    def setup_url(self):
        return self.json['assets'][0]['browser_download_url']

    @property
    def tag(self):
        return self.json['tag_name']

    @property
    def author(self):
        return self.json['author']['login']

    @property
    def description(self):
        return self.json['body']

    @property
    def is_draft(self):
        return self.json['draft']

    @property
    def version(self):
        return Version(self.tag)
