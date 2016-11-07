# coding=utf-8
import os
import time
import random
import string

import pytest
from blinker_herald import signals

from src.cache.cache import Cache, CacheEvent
from src.low.custom_path import Path
from src.low.singleton import Singleton


class TestCache:
    @pytest.fixture(autouse=True)
    def wipe_cache(self):
        Singleton.wipe_instances('Cache')

    @pytest.fixture(params=list(range(20)))
    def random_names(self, request, tmpdir):
        """This is *very* costly to run but is there to ensure stability of the cache and catch corner instability
        with the FSObserver"""
        names = (
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
        )
        yield names
        Cache().stop()
        tmpdir.remove()

    def test_cache_init(self, tmpdir):
        with pytest.raises(ValueError):
            Cache()
        td = str(tmpdir)
        Cache(td)

    def test_cache_creates_own_directory(self, tmpdir):
        td = str(tmpdir.join('x'))
        assert not os.path.exists(td)
        Cache(td)
        assert os.path.exists(td)

    def test_on_moved(self, tmpdir, qtbot):
        signal_caught = False
        td = str(tmpdir)
        random_files = []
        for x in range(1):
            p = Path(tmpdir.join('f{}'.format(x)))
            p.write_text('')
            random_files.append(p)
        c = Cache(td)
        while c.is_building:
            time.sleep(0.1)
        new_p = Path(str(tmpdir.join('ff')))

        def got_signal(sender, signal_emitter, event):
            nonlocal signal_caught
            assert sender == 'Cache'
            assert isinstance(signal_emitter, Cache)
            assert isinstance(event, CacheEvent)
            assert signal_emitter is c
            try:
                assert event.event_type == 'moved'
            except AssertionError:
                assert event.event_type == 'modified'
                assert event.src == new_p.abspath()
            else:
                assert event.src == old_p.abspath()
                assert event.dst == new_p.abspath()
                assert not old_p.abspath() in c
                assert new_p.abspath() in c
                signal_caught = True

        signals.post_cache_changed_event.connect(got_signal)

        old_p = random_files[0]
        assert isinstance(old_p, Path)
        old_p.rename(new_p.abspath())

        qtbot.wait_until(lambda: signal_caught is True, timeout=5000)

        signals.post_cache_changed_event.disconnect(got_signal)

    def test_on_created(self, tmpdir, qtbot):
        signal_caught = False
        td = str(tmpdir)

        c = Cache(td)

        p = Path(tmpdir.join('f'))

        def got_signal(sender, signal_emitter, event):
            nonlocal signal_caught
            assert sender == 'Cache'
            assert isinstance(signal_emitter, Cache)
            assert isinstance(event, CacheEvent)
            assert signal_emitter is c
            assert event.event_type == 'created'
            assert event.src == p.abspath()
            assert p.abspath() in c
            assert len(c) == 1
            signal_caught = True

        signals.post_cache_changed_event.connect(got_signal)

        assert not os.path.exists(p.abspath())
        assert p.abspath() not in c
        assert len(c) == 0
        p.write_text('')
        assert os.path.exists(p.abspath())
        qtbot.wait_until(lambda: signal_caught is True, timeout=5000)

        signals.post_cache_changed_event.disconnect(got_signal)

        assert p.abspath() in c
        assert os.path.exists(p.abspath())

    def test_on_deleted(self, tmpdir, qtbot):
        signal_caught = False
        td = str(tmpdir)
        p = Path(tmpdir.join('f'))
        p.write_text('')

        c = Cache(td)
        print(c.meta)

        def got_signal(sender, signal_emitter, event):
            nonlocal signal_caught
            assert sender == 'Cache'
            assert isinstance(signal_emitter, Cache)
            assert isinstance(event, CacheEvent)
            assert signal_emitter is c
            assert event.event_type == 'deleted'
            assert event.src == p.abspath()
            assert not p.abspath() in c
            signal_caught = True

        assert os.path.exists(p.abspath())
        assert os.path.relpath(p.abspath(), td)
        signals.post_cache_changed_event.connect(got_signal)
        print(p.abspath())
        qtbot.wait_until(lambda: p.abspath() in c, timeout=5000)
        assert len(c) == 1
        p.remove()
        assert not os.path.exists(p.abspath())
        qtbot.wait_until(lambda: signal_caught is True, timeout=5000)
        assert len(c) == 0

        signals.post_cache_changed_event.disconnect(got_signal)

    def test_git_dir(self, tmpdir, qtbot, random_names):
        git_file = random_names[0]
        git_dir = random_names[1]
        some_file = random_names[2]
        some_dir = random_names[3]
        td = str(tmpdir)
        p = Path(tmpdir.join('f'))
        p.write_text('')
        g = Path(tmpdir.mkdir('.git'))
        gf = Path(tmpdir.join('.git').join(git_file))
        gf.write_text('')
        gd = Path(tmpdir.join('.git').mkdir(git_dir))
        d = Path(tmpdir.mkdir(some_dir))
        df = Path(tmpdir.join(some_dir).join(some_file))
        df.write_text('')

        cache_built = False

        # noinspection PyUnusedLocal
        @signals.post_cache_build.connect
        def cache_build_done(sender, signal_emitter, **kwargs):
            nonlocal cache_built
            cache_built = True

        c = Cache(td)
        qtbot.wait_until(lambda: cache_built is True)
        assert p.abspath() in c
        assert df.abspath() in c
        assert not d.abspath() in c
        assert not g.abspath() in c
        assert not gd.abspath() in c
        assert not gf.abspath() in c

    def test_temp_file(self, tmpdir, random_names):
        td = str(tmpdir)
        Cache(td)
        for name in random_names:
            tmp_file = Cache().temp_file(subdir=name)
            assert tmp_file.exists()
            assert tmp_file.isfile()

    def test_temp_dir(self, tmpdir, random_names):
        td = str(tmpdir)
        Cache(td)
        for name in random_names:
            tmp_file = Cache().temp_dir(subdir=name)
            assert tmp_file.exists()
            assert tmp_file.isdir()

    def test_wipe_temp(self, tmpdir, random_names):
        td = str(tmpdir)
        Cache(td)
        files = set()
        for name in random_names:
            tmp_file = Cache().temp_file(subdir=name)
            assert tmp_file.exists()
            files.add(tmp_file)
        Cache().stop()
        Cache(td)
        Cache().wipe_temp()
        for file in files:
            assert not file.exists()