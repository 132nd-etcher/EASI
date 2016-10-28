# coding=utf-8

import os
from unittest import mock

from hypothesis import given, settings, example
from hypothesis import strategies as st
# noinspection PyProtectedMember
from src.meta.meta_property import _MetaProperty, MetaProperty
from src.meta.meta import Meta

from src.low.custom_path import Path
from src.meta.meta_singleton import MetaSingleton

from .utils import ContainedTestCase


class DummyMeta(Meta):
    @property
    def meta_header(self):
        return 'DUMMY_META'


class DummySingletonMeta(MetaSingleton):
    @property
    def meta_header(self):
        return 'DUMMY_SINGLETON_META'


def st_any_base():
    return st.one_of(st.floats(), st.integers(), st.text(), st.booleans(), st.none(), st.binary())


def st_any():
    return st.one_of(st.floats(), st.integers(), st.text(), st.booleans(), st.none(), st.binary(),
                     st.lists(st_any_base()), st.dictionaries(st_any_base(), st_any_base()))


class TestMeta(ContainedTestCase):

    def setUp(self):
        super(TestMeta, self).setUp()
        self.temp_file = self.create_temp_file()
        self.meta = DummyMeta(self.temp_file, auto_read=False)

    def test_init(self):
        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            DummyMeta()

    def test_init_with_str(self):
        DummyMeta(self.create_temp_file(), auto_read=False)

    @given(x=st.one_of(st.booleans(), st.none(), st.integers(), st.floats()))
    def test_path_set(self, x):
        p = self.create_temp_file()
        m = DummyMeta(p.abspath(), auto_read=False)
        m.path = p.abspath()
        m.path = Path(str(p.abspath()))
        with self.assertRaises(TypeError):
            m.path = x

    @given(d=st.dictionaries(
        st.one_of(st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()),
        st.one_of(st.booleans(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text()),
        min_size=1)
    )
    def test_context(self, d):
        m = DummyMeta(self.create_temp_file(), init_dict=d, auto_read=False)
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
        m = DummyMeta(self.create_temp_file(), init_dict=d, auto_read=False)
        self.assertSequenceEqual([x for x in m], [x for x in d])
        for x in d.keys():
            self.assertTrue(x in m)

    @given(x=st.one_of(st.booleans(), st.none(), st.integers(), st.floats(), st.text()))
    def test_set_data(self, x):
        m = DummyMeta(self.create_temp_file())
        with self.assertRaises(TypeError):
            m.data = x

    def test_init_with_path(self):
        p = Path(self.create_temp_file())
        self.assertIsInstance(p, Path)
        DummyMeta(p, auto_read=False)

    @given(x=st.one_of(st.booleans(), st.floats(), st.integers(), st.none()))
    def test_init_wrong_arg(self, x):
        with self.assertRaises(TypeError):
            DummyMeta(x, auto_read=False)

    @given(d=st.dictionaries(st.text(), st_any()))
    def test_init_d(self, d):
        DummyMeta('./test_d', init_dict=d, auto_read=False)

    @given(x=st.one_of(st.floats(), st.integers(), st.text(), st.booleans(), st.binary()))
    def test_wrong_init_d(self, x):
        with self.assertRaises(TypeError):
            DummyMeta('./test_d', init_dict=x, auto_read=False)

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
        meta = DummyMeta(self.temp_file, auto_read=False)
        self.assertFalse(self.meta == meta)
        meta.read()
        meta.data['header'] = 'DUMMY_META'
        self.assertDictEqual(self.meta.data, meta.data)

    @given(b=st.integers(min_value=1, max_value=1))
    @settings(max_examples=50)
    def test_corrupted_file(self, **_):
        p = self.create_temp_file()
        with open(p, 'wb') as f:
            f.write(os.urandom(1024 * 32))
        meta = DummyMeta(p, auto_read=False)
        with self.assertRaises(ValueError):
            meta.read()

    @given(d=st.dictionaries(st.text(), st_any()))
    def test_props(self, d):
        p = Path(self.create_temp_file())
        m = DummyMeta(p, init_dict=d, auto_read=False)
        assert p.abspath() == m.path.abspath()
        # self.assertIs p.abspath() == m.path.abspath())
        self.assertIs(d, m.data)
        self.assertIs(d.__len__(), m.__len__())

    @mock.patch('src.low.custom_path.Path.remove')
    def test_empty(self, m):
        assert isinstance(m, mock.MagicMock)
        p = self.create_temp_file()
        open(p.abspath(), 'w').close()
        meta = DummyMeta(p.abspath())
        self.assertEqual(m.call_count, 1)
        meta.read()
        self.assertEqual(m.call_count, 2)
        DummyMeta(p.abspath(), auto_read=False)
        self.assertEqual(m.call_count, 2)

    @given(x=st.one_of(st.text(), st.integers(), st.floats(), st.none()))
    @example(x='')
    def test_decorators_basic(self, x):
        f = mock.MagicMock()
        f.__name__ = 'mock'
        p = _MetaProperty(f, None, bool)
        p.__set__(None, True)
        with self.assertRaises(TypeError):
            p.__set__(self, x)
        self.assertIs(p.__get__(None, None), p)

    @given(x=st.one_of(st.booleans(), st.integers(), st.floats(), st.none()))
    def test_decorators_implemented(self, x):

        f = mock.MagicMock()
        f.__name__ = 'mock'

        class C(Meta):
            @property
            def meta_header(self):
                return 'test_meta'

            @MetaProperty('default', str)
            def some_prop(self, _):
                f('mock called')

        c = C(self.create_temp_file())
        self.assertSequenceEqual(c.some_prop, 'default')
        with self.assertRaises(TypeError):
            c.some_prop = x
        self.assertEqual(f.call_count, 0)
        c.some_prop = 'text'
        self.assertSequenceEqual(c.some_prop, 'text')
        self.assertEqual(f.call_count, 1)

    def test_singleton_meta(self):
        p = self.create_temp_file()
        m1 = DummySingletonMeta(p)
        m2 = DummySingletonMeta(str(p.abspath()))
        self.assertTrue(m1 is m2)

    @given(x=st.one_of(st.booleans(), st.integers(), st.none(), st.floats()))
    def test_single_meta_wrong_type(self, x):
        with self.assertRaises(TypeError):
            DummySingletonMeta(x)
