# coding=utf-8
import unittest

from hypothesis import strategies as st, given
from src.low.version import Version


class TestCustomVersion(unittest.TestCase):
    def setUp(self):
        pass

    def test_custom_version_creation(self):
        with self.assertRaises(ValueError):
            Version()
        for wrong_Version_str in ['0.0.0', '0.0.0.0.0', 'some_str']:
            with self.assertRaises(ValueError):
                Version(wrong_Version_str)
        for x in [0.0, None, True]:
            with self.assertRaises(ValueError):
                Version(x)
        v = Version('1.2.3.4')
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.revision, 3)
        self.assertEqual(v.build, 4)

    def test_version_comparison(self):
        v1 = Version('1.0.0.0')
        v2 = Version('1.2.3.4')
        v3 = Version('1.3.3.4')
        v4 = Version('1.4.4.4')
        v5 = Version('1.5.0.0')
        v6 = Version('2.2.3.5')
        v7 = Version('2.2.4.5')
        v8 = Version('2.2.4.6')
        self.assertGreater(v2, v1)
        self.assertLess(v1, v2)
        self.assertGreater(v3, v2)
        self.assertGreater(v4, v3)
        self.assertGreater(v5, v4)
        self.assertGreater(v6, v5)
        self.assertLess(v4, v5)
        self.assertLess(v5, v6)
        self.assertLess(v6, v7)
        self.assertGreater(v7, v6)
        self.assertLess(v7, v8)
        for v in [v1, v2, v3, v4, v5, v6, v7, v8]:
            self.assertEqual(v, v)

    @given(
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
    )
    def test_custom_version_repr(self, m, mm, b, r):
        v = Version('.'.join([str(x) for x in [m, mm, b, r]]))
        self.assertEqual(v.__repr__(), 'Version(\'{}\')'.format('.'.join([str(x) for x in [m, mm, b, r]])))

    @given(
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
    )
    def test_init_from_integers(self, m, mm, b, r):
        Version(major=m, minor=mm, build=b, revision=r)

    @given(
        st.integers(min_value=10),
        st.integers(min_value=10),
        st.integers(min_value=10),
        st.integers(min_value=10),
    )
    def test_reset(self, m, mm, b, r):
        v = Version(major=m, minor=mm, build=b, revision=r)
        self.assertNotEqual(v.build, 0)
        v.reset_build()
        self.assertEqual(v.build, 0)
        self.assertNotEqual(v.revision, 0)
        v.reset_revision()
        self.assertEqual(v.revision, 0)
        self.assertNotEqual(v.minor, 0)
        v.reset_minor()
        self.assertEqual(v.minor, 0)

    @given(
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
    )
    def test_bump(self, m, mm, b, r):
        v = Version(major=m, minor=mm, build=b, revision=r)
        v.bump_build()
        self.assertEqual(v.build, b+1)
        v.bump_revision()
        self.assertEqual(v.revision, r+1)
        v.bump_major()
        self.assertEqual(v.major, m+1)
        v.bump_minor()
        self.assertEqual(v.minor, mm+1)

    @given(
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
        st.integers(min_value=0),
    )
    def test_to_tuple(self, m, mm, b, r):
        v = Version(major=m, minor=mm, build=b, revision=r)
        self.assertSequenceEqual(v.to_tuple(), tuple([m, mm, r, b]))

    @given(st.lists(st.one_of(st.booleans(), st.text(), st.floats()), max_size=4))
    def test_wrong_init(self, x):
        with self.assertRaises(ValueError):
            Version(*x)

    def tearDown(self):
        pass
