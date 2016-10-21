# coding=utf-8
import os
import time

import pytest
from blinker_herald import signals

from src.cache.cache import Cache, CacheEvent
from src.low.custom_path import Path
from src.low.singleton import Singleton


class TestCache:
    @pytest.fixture(autouse=True)
    def wipe_singleton(self):
        Singleton.wipe_instances()
        yield
        Singleton.wipe_instances()

    def test_cache_init(self, tmpdir):
        Singleton.wipe_instances()
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
        """
        This one is a little special: Cache will generate two events during the move, one expected "move" event,
        and another "modified" event for the destination of the move.

        Thus, the signal catching function will run twice and throw an AssertionError; it is expected behaviour and
        safe to ignore.
        """

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

        @signals.post_cache_changed_event.connect
        def got_signal(sender, signal_emitter, event):
            nonlocal signal_caught
            assert sender == 'Cache'
            assert isinstance(signal_emitter, Cache)
            assert isinstance(event, CacheEvent)
            assert signal_emitter is c
            assert event.event_type == 'moved'
            assert event.src == old_p.abspath()
            assert event.dst == new_p.abspath()
            assert not old_p.abspath() in c
            assert new_p.abspath() in c
            signal_caught = True

        old_p = random_files[0]
        assert isinstance(old_p, Path)
        old_p.rename(new_p.abspath())

        qtbot.wait_until(lambda: signal_caught is True)

    def test_on_created(self, tmpdir, qtbot):
        signal_caught = False
        td = str(tmpdir)

        c = Cache(td)

        p = Path(tmpdir.join('f'))

        @signals.post_cache_changed_event.connect
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

        assert not os.path.exists(p.abspath())
        assert len(c) == 0
        p.write_text('')
        assert os.path.exists(p.abspath())
        qtbot.wait_until(lambda: signal_caught is True)

    def test_on_deleted(self, tmpdir, qtbot):
        signal_caught = False
        td = str(tmpdir)
        p = Path(tmpdir.join('f{}'))
        p.write_text('')

        c = Cache(td)

        @signals.post_cache_changed_event.connect
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

        assert p.abspath() in c
        assert len(c) == 1
        p.remove()
        assert not os.path.exists(p.abspath())
        qtbot.wait_until(lambda: signal_caught is True)
        assert len(c) == 0
