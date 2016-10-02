# coding=utf-8

from unittest import TestCase
from src.low.epoch import Epoch


class TestEpoch(TestCase):

    def test_online_epoch(self):
        cached_epoch = Epoch.epoch_cached_online()
        epoch = Epoch.epoch_online()
        self.assertTrue(epoch > cached_epoch)
        epoch = Epoch.epoch_cached_online()
        self.assertEqual(cached_epoch, epoch)
