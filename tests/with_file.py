# coding=utf-8
from unittest import TestCase


class TestCaseWithTestFile(TestCase):

    test_file = './test'

    def remove_file(self):
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def setUp(self):
        self.remove_file()

    def tearDown(self):
        self.remove_file()
