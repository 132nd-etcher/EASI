# coding=utf-8

import time
from src.low.epoch import Epoch


class TestEpoch:

    def test_online_epoch(self):
        cached_epoch = Epoch.epoch_cached_online()
        time.sleep(1)
        epoch = Epoch.epoch_online()
        assert epoch > cached_epoch
        epoch = Epoch.epoch_cached_online()
        assert cached_epoch, epoch
