# coding=utf-8

import os
from unittest import TestCase
from unittest import mock

from hypothesis import given, settings, example
from hypothesis import strategies as st

from src.low.custom_path import Path
from src.low.meta.decorators import meta_property, meta_property_with_default
from src.low.meta.meta import Meta
from src.low.meta.meta_singleton import MetaSingleton

from src.low.custom_logging import make_logger

logger = make_logger(__name__)


def st_any_base():
    return st.one_of(st.floats(), st.integers(), st.text(), st.booleans(), st.none(), st.binary())


def st_any():
    return st.one_of(st.floats(), st.integers(), st.text(), st.booleans(), st.none(), st.binary(),
                     st.lists(st_any_base()), st.dictionaries(st_any_base(), st_any_base()))


# noinspection PyUnresolvedReferences
class TestMeta(TestCase):
    to_del = ['./test', './test_b', './test_d', './test_t']

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)

        for x in TestMeta.to_del:
            if os.path.exists(x):
                os.remove(x)

    def setUp(self):
        self.meta = Meta('./test', auto_read=False)

    def tearDown(self):
        del self.meta
        for x in TestMeta.to_del:
            if os.path.exists(x):
                os.remove(x)

    def test_init(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            Meta()

    def test_init_with_str(self):
        Meta('./test', auto_read=False)

    @given(x=st.one_of(st.booleans(), st.none(), st.integers(), st.floats()))
    def test_path_set(self, x):
        m = Meta('./test', auto_read=False)
        m.path = './test'
        m.path = Path('./test')
        with self.assertRaises(TypeError):
            m.path = x

    @given(d=st.dictionaries(
        st.one_of(st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()),
        st.one_of(st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()),
        min_size=1)
    )
    def test_context(self, d):
        m = Meta('./test_d', init_dict=d, auto_read=False)
        self.assertDictEqual(d, m.get_context())

    @given(d=st.dictionaries(
        st.one_of(st.text(), st.integers()),
        st.one_of(st.text(), st.none(), st.floats(), st.integers(), st.booleans()),
        average_size=5,
        min_size=1
    )
    )
    def test_dict_props(self, d):
        assert isinstance(d, dict)
        m = Meta('./test_d', init_dict=d, auto_read=False)
        logger.critical(d)
        self.assertSequenceEqual([x for x in m], [x for x in d])
        for x in d.keys():
            self.assertTrue(x in m)

    @given(x=st.one_of(st.booleans(), st.none(), st.integers(), st.floats(), st.text()))
    def test_set_data(self, x):
        m = Meta('./test')
        with self.assertRaises(TypeError):
            m.data = x

    def test_init_with_path(self):
        p = Path('./test')
        self.assertIsInstance(p, Path)
        Meta(p, auto_read=False)

    @given(x=st.one_of(st.booleans(), st.floats(), st.integers(), st.none()))
    def test_init_wrong_arg(self, x):
        with self.assertRaises(TypeError):
            Meta(x, auto_read=False)

    @given(d=st.dictionaries(st.text(), st_any()))
    def test_init_d(self, d):
        Meta('./test_d', init_dict=d, auto_read=False)

    @given(x=st.one_of(st.floats(), st.integers(), st.text(), st.booleans(), st.binary()))
    def test_wrong_init_d(self, x):
        with self.assertRaises(TypeError):
            Meta('./test_d', init_dict=x, auto_read=False)

    def test_write_empty(self):
        with self.assertRaises(ValueError):
            self.meta.write()

    @given(d=st.dictionaries(
        st.one_of(st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()),
        st.one_of(st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()),
        min_size=1
    ))
    def test_write_basic(self, d):
        self.meta.data = d
        self.meta.write()
        meta = Meta('./test', auto_read=False)
        self.assertFalse(self.meta == meta)
        meta.read()
        self.assertDictEqual(self.meta.data, meta.data)

    @given(b=st.integers(min_value=1, max_value=1))
    @settings(max_examples=50)
    def test_corrupted_file(self, **_):
        with open('./test_b', 'wb') as f:
            f.write(os.urandom(1024 * 32))
        meta = Meta('./test_b', auto_read=False)
        with self.assertRaises(ValueError):
            meta.read()

    @given(d=st.dictionaries(st.text(), st_any()))
    def test_props(self, d):
        p = Path('./test')
        m = Meta(p, init_dict=d, auto_read=False)
        self.assertIs(p, m.path)
        self.assertIs(d, m.data)
        self.assertIs(d.__len__(), m.__len__())

    @mock.patch('src.low.custom_path.Path.remove')
    def test_empty(self, m):
        assert isinstance(m, mock.MagicMock)
        open('./test_t', 'w').close()
        meta = Meta('./test_t')
        self.assertEqual(m.call_count, 1)
        meta.read()
        self.assertEqual(m.call_count, 2)
        Meta('./test_t', auto_read=False)
        self.assertEqual(m.call_count, 2)

    @given(x=st.one_of(st.text(), st.integers(), st.floats(), st.none()))
    @example(x='')
    def test_decorators_basic(self, x):
        f = mock.MagicMock()
        f.__name__ = 'mock'
        p = meta_property(f, None, bool)
        p.__set__(None, True)
        with self.assertRaises(TypeError):
            p.__set__(None, x)
        self.assertIs(p.__get__(None, None), p)

    @given(x=st.one_of(st.booleans(), st.integers(), st.floats(), st.none()))
    def test_decorators_implemented(self, x):

        f = mock.MagicMock()
        f.__name__ = 'mock'

        class C(Meta):
            @meta_property_with_default('default', str)
            def some_prop(self, _):
                f('mock called')

        c = C('./test')
        self.assertSequenceEqual(c.some_prop, 'default')
        with self.assertRaises(TypeError):
            c.some_prop = x
        self.assertEqual(f.call_count, 0)
        c.some_prop = 'text'
        self.assertEqual(f.call_count, 1)

    def test_singleton_meta(self):
        m1 = MetaSingleton('./test')
        m2 = MetaSingleton(Path('./test'))
        self.assertTrue(m1 is m2)

    @given(x=st.one_of(st.booleans(), st.integers(), st.none(), st.floats()))
    def test_single_meta_wrong_type(self, x):
        with self.assertRaises(TypeError):
            MetaSingleton(x)
