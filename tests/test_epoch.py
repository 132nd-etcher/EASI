# coding=utf-8

import time
from unittest import TestCase
from src.low.epoch import Epoch


class TestEpoch(TestCase):

    def test_online_epoch(self):
        cached_epoch = Epoch.epoch_cached_online()
        time.sleep(1)
        epoch = Epoch.epoch_online()
        self.assertTrue(epoch > cached_epoch)
        epoch = Epoch.epoch_cached_online()
        self.assertEqual(cached_epoch, epoch)
