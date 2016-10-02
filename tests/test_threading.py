# coding=utf-8

import time
from unittest import TestCase, mock

from hypothesis import strategies as st, given, example

from src.threadpool import ThreadPool


class TestThreading(TestCase):
    def sleep(self, t=0.1):
        time.sleep(t)

    def test_join(self):
        p = ThreadPool(1, 'test', False)
        p.queue_task(self.sleep)
        p.join_all()

    def test_force_join(self):
        start = time.time()
        p = ThreadPool(1, 'test', False)
        p.queue_task(self.sleep, [10])
        p.join_all(False, False)
        self.assertTrue(time.time() - start < 2)

    def test_decrease_pool_size(self):
        p = ThreadPool(10)
        p.set_thread_count(0)

    @given(x=st.one_of(st.booleans(), st.text(), st.none(), st.integers(), st.floats()))
    @example(x=None)
    def test_queue_wrong_task_type(self, x):
        p = ThreadPool(1, 'test', True)
        with self.assertRaises(ValueError):
            p.queue_task(x)
        p.join_all(False, False)

    def test_queue_task(self):
        p = ThreadPool(10, 'test', True)

        def some_func():
            return True

        for x in range(100):
            self.assertTrue(p.queue_task(some_func))
        p.join_all()
        time.sleep(0.1)
        self.assertTrue(p.all_done())