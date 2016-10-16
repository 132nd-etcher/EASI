# coding=utf-8
import os
from unittest import mock

from PyQt5.QtTest import QTest
from pytestqt.qtbot import QtBot

from src.cfg import config
from src.low import constants
from src.qt import Qt
from src.ui.dialog_config import ConfigDialog

constants.TESTING = True

k = mock.patch('src.cfg.values.sig_cfg_keyring_encrypt', value_changed=mock.MagicMock())
a = mock.patch('src.cfg.values.sig_cfg_author_mode', value_changed=mock.MagicMock())
s = mock.patch('src.cfg.values.sig_cfg_sg_path', value_changed=mock.MagicMock())
c = mock.patch('src.cfg.values.sig_cfg_cache_path', value_changed=mock.MagicMock())
kd = mock.patch('src.cfg.values.sig_cfg_kdiff_path', value_changed=mock.MagicMock())
t = mock.patch('src.cfg.values.sig_cfg_subscribe_to_test_versions', value_changed=mock.MagicMock())

sig_kdiff_path_changed = kd.start()
sig_cache_path_changed = c.start()
sig_sg_path_changed = s.start()
sig_author_mode = a.start()
sig_keyring = k.start()
sig_cfg_subscribe_to_test_versions = t.start()


def setup_valid_dialog(tmpdir):
    sg = str(tmpdir.mkdir('sg'))
    cache = str(tmpdir.mkdir('cache'))
    kdiff = tmpdir.join('kdiff3.exe')
    kdiff.write('')
    kdiff = str(kdiff)
    config.saved_games_path = sg
    config.cache_path = cache
    config.kdiff_path = kdiff
    dialog = ConfigDialog()
    dialog.show()
    dialog.setup()
    return dialog, sg, cache, kdiff


def test_config_dialog_signals(qtbot: QtBot, tmpdir):
    dialog, _, _, _ = setup_valid_dialog(tmpdir)
    qtbot.addWidget(dialog)
    dialog.save_settings()

    def check_signal_called():
        sig_keyring.value_changed.assert_called_with(dialog.check_box_encrypt.isChecked())
        sig_author_mode.value_changed.assert_called_with(dialog.author_mode.isChecked())
        sig_sg_path_changed.value_changed.assert_called_with(dialog.sg_line_edit.text())
        sig_cache_path_changed.value_changed.assert_called_with(dialog.cache_line_edit.text())
        sig_kdiff_path_changed.value_changed.assert_called_with(dialog.kdiff_line_edit.text())
        sig_cfg_subscribe_to_test_versions.value_changed.assert_called_with(
            dialog.subscribe_to_test_versions.isChecked())

    qtbot.wait_until(check_signal_called)


def test_sg_path(qtbot: QtBot, tmpdir, mocker):
    assert isinstance(qtbot, (QtBot, QTest))
    test_dir = str(tmpdir.mkdir('t'))
    test_file = tmpdir.join('file')
    test_file.write('')
    dialog, sg, cache, kdiff = setup_valid_dialog(tmpdir)

    assert config.saved_games_path == dialog.sg_line_edit.text()

    assert dialog.btn_apply.isEnabled() is False

    assert dialog.config_settings['sg_path'].value_default is None
    assert dialog.config_settings['sg_path'].value_type is str

    dialog.sg_line_edit.clear()
    qtbot.keyClicks(dialog.sg_line_edit, str(tmpdir.join('caribou')), Qt.NoModifier)

    qtbot.wait_signal(dialog.sg_line_edit.textChanged)

    def apply_btn_active():
        assert dialog.btn_apply.isEnabled() is True

    qtbot.wait_until(apply_btn_active)

    dialog.save_settings()

    def check_balloons():
        assert len(dialog.config_settings['sg_path'].balloons) == 1

    qtbot.wait_until(check_balloons)

    config.saved_games_path = test_dir
    dialog.load_settings()
    assert dialog.sg_line_edit.text() == test_dir

    dialog.sg_line_edit.clear()
    qtbot.keyClicks(dialog.sg_line_edit, test_dir, Qt.NoModifier)
    assert dialog.sg_line_edit.text() == test_dir

    def config_updated():
        assert config.saved_games_path == test_dir

    qtbot.mouseClick(dialog.buttonBox.button(dialog.buttonBox.Apply), Qt.LeftButton)
    qtbot.wait_until(config_updated)

    show_error_balloon = mocker.spy(dialog.config_settings['sg_path'], 'show_error_balloon')

    save_settings = mocker.spy(dialog, 'save_settings')

    dialog.sg_line_edit.clear()
    qtbot.keyClicks(dialog.sg_line_edit, str(tmpdir.join('some_path')), Qt.NoModifier)

    assert dialog.buttonBox.button(dialog.buttonBox.Apply).isEnabled()
    assert dialog.sg_line_edit.text() == str(tmpdir.join('some_path'))

    qtbot.wait_until(apply_btn_active)
    qtbot.mouseClick(dialog.buttonBox.button(dialog.buttonBox.Apply), Qt.LeftButton)

    def settings_saved():
        assert save_settings.called

    qtbot.wait_until(settings_saved)

    show_error_balloon.reset_mock()
    save_settings.reset_mock()

    dialog.sg_line_edit.clear()
    qtbot.keyClicks(dialog.sg_line_edit, test_dir, Qt.NoModifier)
    qtbot.mouseClick(dialog.buttonBox.button(dialog.buttonBox.Apply), Qt.LeftButton)

    with mock.patch('os.startfile') as m:
        dialog.config_settings['sg_path'].show_in_explorer()
        m.assert_called_with(test_dir)

    with mock.patch('src.ui.dialog_browse.dialog.BrowseDialog.get_directory') as m:
        dialog.config_settings['sg_path'].browse_for_value()
        m.assert_called_with(
            init_dir=test_dir,
            title='Select your {} directory'.format(dialog.config_settings['sg_path'].dir_name()),
            parent=dialog
        )


def test_cancel(qtbot, tmpdir):
    dialog, sg, cache, kdiff = setup_valid_dialog(tmpdir)

    assert config.saved_games_path == sg
    assert dialog.sg_line_edit.text() == sg
    assert config.cache_path == cache
    assert dialog.cache_line_edit.text() == cache
    assert config.kdiff_path == kdiff
    assert dialog.kdiff_line_edit.text() == kdiff

    test_dir = str(tmpdir.mkdir('moo'))
    test_file = tmpdir.join('file')
    test_file.write('')
    test_file = str(test_file)
    dialog.sg_line_edit.setText(test_dir)
    dialog.cache_line_edit.setText(test_dir)
    dialog.kdiff_line_edit.setText(test_file)
    qtbot.mouseClick(dialog.btn_cancel, Qt.LeftButton)

    assert dialog.isVisible() is False

    assert config.saved_games_path == sg
    assert dialog.sg_line_edit.text() == test_dir
    assert config.cache_path == cache
    assert dialog.cache_line_edit.text() == test_dir
    assert config.kdiff_path == kdiff
    assert dialog.kdiff_line_edit.text() == test_file


def test_ok(qtbot, tmpdir):
    dialog, sg, cache, kdiff = setup_valid_dialog(tmpdir)

    assert config.saved_games_path == sg
    assert dialog.sg_line_edit.text() == sg
    assert config.cache_path == cache
    assert dialog.cache_line_edit.text() == cache
    assert config.kdiff_path == kdiff
    assert dialog.kdiff_line_edit.text() == kdiff

    test_dir = str(tmpdir.mkdir('moo'))
    test_file = tmpdir.join('kdiff3.exe')
    test_file.write('')
    test_file = str(test_file)
    dialog.sg_line_edit.setText(test_dir)
    dialog.cache_line_edit.setText(test_dir)
    dialog.kdiff_line_edit.setText(test_file)
    qtbot.mouseClick(dialog.btn_ok, Qt.LeftButton)

    assert dialog.isVisible() is False

    assert config.saved_games_path == test_dir
    assert dialog.sg_line_edit.text() == test_dir
    assert config.cache_path == test_dir
    assert dialog.cache_line_edit.text() == test_dir
    assert config.kdiff_path == test_file
    assert dialog.kdiff_line_edit.text() == test_file


def test_reset(qtbot, tmpdir):
    dialog, sg, cache, kdiff = setup_valid_dialog(tmpdir)

    assert config.saved_games_path == sg
    assert dialog.sg_line_edit.text() == sg
    assert config.cache_path == cache
    assert dialog.cache_line_edit.text() == cache
    assert config.kdiff_path == kdiff
    assert dialog.kdiff_line_edit.text() == kdiff

    test_dir = str(tmpdir.mkdir('moo'))
    test_file = tmpdir.join('kdiff3.exe')
    test_file.write('')
    test_file = str(test_file)
    dialog.sg_line_edit.setText(test_dir)
    dialog.cache_line_edit.setText(test_dir)
    dialog.kdiff_line_edit.setText(test_file)
    qtbot.mouseClick(dialog.btn_reset, Qt.LeftButton)

    assert config.saved_games_path == sg
    assert dialog.sg_line_edit.text() == sg
    assert config.cache_path == cache
    assert dialog.cache_line_edit.text() == cache
    assert config.kdiff_path == kdiff
    assert dialog.kdiff_line_edit.text() == kdiff


def test_directory_does_not_exist(qtbot, tmpdir, mocker):
    dialog, sg, cache, _ = setup_valid_dialog(tmpdir)

    p = str(tmpdir.join('dir'))

    assert os.path.exists(p) is False

    save_settings = mocker.spy(dialog, 'save_settings')

    for qt_object, cfg_value, obj_name in {
        (dialog.sg_line_edit, sg, 'sg_path'),
        (dialog.cache_line_edit, cache, 'cache_path'),
    }:
        dialog.setup()

        show_error_balloon = mocker.spy(dialog.config_settings[obj_name], 'show_error_balloon')

        assert qt_object.text() == cfg_value

        qt_object.clear()
        qtbot.keyClicks(qt_object, p)
        qtbot.mouseClick(dialog.btn_apply, Qt.LeftButton)

        def settings_saved():
            save_settings.assert_called_with()

        qtbot.wait_until(settings_saved)

        show_error_balloon.assert_called_with('Directory does not exist')


def test_not_a_directory(qtbot, tmpdir, mocker):
    dialog, sg, cache, _ = setup_valid_dialog(tmpdir)

    p = tmpdir.join('dir')
    p.write('')
    p = str(p)

    assert os.path.exists(p) is True
    assert os.path.isfile(p) is True

    save_settings = mocker.spy(dialog, 'save_settings')

    for qt_object, cfg_value, obj_name in {
        (dialog.sg_line_edit, sg, 'sg_path'),
        (dialog.cache_line_edit, cache, 'cache_path'),
    }:
        dialog.setup()

        show_error_balloon = mocker.spy(dialog.config_settings[obj_name], 'show_error_balloon')

        assert qt_object.text() == cfg_value

        qt_object.clear()
        qtbot.keyClicks(qt_object, p)
        qtbot.mouseClick(dialog.btn_apply, Qt.LeftButton)

        def settings_saved():
            save_settings.assert_called_with()

        qtbot.wait_until(settings_saved)

        def show_error_called():
            show_error_balloon.assert_called_with('Not a directory')

        qtbot.wait_until(show_error_called)
