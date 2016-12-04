# coding=utf-8
from src.low.custom_path import Path


class CacheEvent:
    """
    Represents an event sent by the Cache when the watched filesystem is changed
    """

    def __init__(self, event_type: str, src: str, dst: str = None):
        self.event_type = event_type
        self.src = Path(src)
        self.dst = Path(dst) if dst else dst

    def __str__(self):
        return '{}: {}'.format(
            self.event_type, self.src if self.dst is None else '{} -> {}'.format(
                self.src, self.dst))

    def filter(self, path: str or Path):
        if isinstance(path, Path):
            path = str(path.abspath())
        if not path.endswith('\\'):
            path += '\\'
        return str(self.src.abspath()).startswith(path)
