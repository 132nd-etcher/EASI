# coding=utf-8
import os
from unittest import mock

import pytest
from blinker import signal
from pytestqt.qtbot import QtBot

from src.low import constants
from src.qt import Qt
from src.ui.dialog_config.dialog import ConfigDialog

constants.TESTING = True


def dummy(*args, **kwargs):
    print(args, kwargs)


sig_kdiff_path_changed = signal('Config_kdiff_path_value_changed')
sig_cache_path_changed = signal('Config_cache_path_value_changed')
sig_saved_games_path_changed = signal('Config_saved_games_path_value_changed')
sig_author_mode_changed = signal('Config_author_mode_value_changed')
sig_encrypt_keyring_changed = signal('Config_encrypt_keyring_value_changed')
sig_subscribe_to_test_versions_changed = signal('Config_subscribe_to_test_versions_value_changed')
kdiff_mock_sig = mock.Mock(spec=dummy)
cache_mock_sig = mock.MagicMock(spec=dummy)
sg_mock_sig = mock.Mock(spec=dummy)
author_mock_sig = mock.Mock(spec=dummy)
encrypt_mock_sig = mock.Mock(spec=dummy)
subscribe_mock_sig = mock.MagicMock(spec=dummy)


class TestConfigDialog:
    dialog = None
    sg = None
    kdiff = None
    cache = None
    config = None

    @pytest.fixture(autouse=True)
    def reset(self, qtbot: QtBot, config_dialog):
        self.dialog, self.sg, self.cache, self.kdiff, self.config = config_dialog
        qtbot.add_widget(self.dialog)
        kdiff_mock_sig.reset_mock()
        cache_mock_sig.reset_mock()
        sg_mock_sig.reset_mock()
        author_mock_sig.reset_mock()
        encrypt_mock_sig.reset_mock()
        subscribe_mock_sig.reset_mock()
        sig_cache_path_changed.connect(cache_mock_sig, weak=False)
        sig_kdiff_path_changed.connect(kdiff_mock_sig, weak=False)
        sig_saved_games_path_changed.connect(sg_mock_sig, weak=False)
        sig_author_mode_changed.connect(author_mock_sig, weak=False)
        sig_encrypt_keyring_changed.connect(encrypt_mock_sig, weak=False)
        sig_subscribe_to_test_versions_changed.connect(subscribe_mock_sig, weak=False)
        yield

    @pytest.fixture()
    def random_line_edit_values(self, tmpdir, qtbot):
        assert self.config.saved_games_path == self.sg
        assert self.dialog.sg_line_edit.text() == self.sg
        assert self.config.cache_path == self.cache
        assert self.dialog.cache_line_edit.text() == self.cache
        assert self.config.kdiff_path == self.kdiff
        assert self.dialog.kdiff_line_edit.text() == self.kdiff
        qtbot.wait_until(lambda: not self.dialog.btn_apply.isEnabled())
        qtbot.wait_until(lambda: not self.dialog.btn_reset.isEnabled())
        test_dir = str(tmpdir.mkdir('moo'))
        test_file = tmpdir.join('kdiff3.exe')
        test_file.write('')
        test_file = str(test_file)
        self.dialog.sg_line_edit.setText(test_dir)
        self.dialog.cache_line_edit.setText(test_dir)
        self.dialog.kdiff_line_edit.setText(test_file)
        return test_dir, test_file

    def test_config_dialog_signals(self, qtbot, tmpdir, config):
        assert isinstance(self.dialog, ConfigDialog)
        self.dialog.save_settings()

        assert config.author_mode == self.dialog.author_mode.isChecked()
        assert config.subscribe_to_test_versions == self.dialog.subscribe_to_test_versions.isChecked()
        assert config.encrypt_keyring == self.dialog.check_box_encrypt.isChecked()
        assert config.saved_games_path == self.dialog.sg_line_edit.text()
        assert config.kdiff_path == self.dialog.kdiff_line_edit.text()
        assert config.cache_path == self.dialog.cache_line_edit.text()

        def check_signals():
            assert subscribe_mock_sig.call_count == 0
            assert encrypt_mock_sig.call_count == 0
            assert author_mock_sig.call_count == 0
            assert sg_mock_sig.call_count == 0
            assert cache_mock_sig.call_count == 0
            assert kdiff_mock_sig.call_count == 0

        qtbot.wait_until(check_signals, timeout=3000)
        self.dialog.subscribe_to_test_versions.setChecked(not self.dialog.subscribe_to_test_versions.isChecked())
        self.dialog.save_settings()

        def check_signals():
            assert subscribe_mock_sig.call_count == 1
            subscribe_mock_sig.assert_called_with('Config', value=self.dialog.subscribe_to_test_versions.isChecked())

        qtbot.wait_until(check_signals, timeout=3000)
        self.dialog.check_box_encrypt.setChecked(not self.dialog.check_box_encrypt.isChecked())
        self.dialog.save_settings()

        def check_signals():
            assert encrypt_mock_sig.call_count == 1
            encrypt_mock_sig.assert_called_with('Config', value=self.dialog.check_box_encrypt.isChecked())

        qtbot.wait_until(check_signals, timeout=3000)
        self.dialog.author_mode.setChecked(not self.dialog.author_mode.isChecked())
        self.dialog.save_settings()

        def check_signals():
            assert author_mock_sig.call_count == 1
            author_mock_sig.assert_called_with('Config', value=self.dialog.author_mode.isChecked())

        qtbot.wait_until(check_signals, timeout=3000)
        self.dialog.sg_line_edit.setText(str(tmpdir))
        self.dialog.save_settings()

        def check_signals():
            assert sg_mock_sig.call_count == 1
            sg_mock_sig.assert_called_with('Config', value=self.dialog.sg_line_edit.text())

        qtbot.wait_until(check_signals, timeout=3000)
        self.dialog.cache_line_edit.setText(str(tmpdir))
        self.dialog.save_settings()

        def check_signals():
            assert cache_mock_sig.call_count == 1
            cache_mock_sig.assert_called_with('Config', value=self.dialog.cache_line_edit.text())

        qtbot.wait_until(check_signals, timeout=3000)
        kdiff = str(tmpdir.mkdir('sub').join('kdiff3.exe'))
        with open(kdiff, 'w') as f:
            f.write('')
        self.dialog.kdiff_line_edit.setText(kdiff)
        self.dialog.save_settings()

        def check_signals():
            assert kdiff_mock_sig.call_count == 1
            kdiff_mock_sig.assert_called_with('Config', value=self.dialog.kdiff_line_edit.text())

        qtbot.wait_until(check_signals, timeout=3000)

    def test_sg_path(self, tmpdir, mocker, qtbot):
        test_dir = str(tmpdir.mkdir('t'))
        test_file = tmpdir.join('file')
        test_file.write('')
        dialog = self.dialog

        assert self.config.saved_games_path == dialog.sg_line_edit.text()

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

        self.config.saved_games_path = test_dir
        dialog.load_settings()
        assert dialog.sg_line_edit.text() == test_dir

        dialog.sg_line_edit.clear()
        qtbot.keyClicks(dialog.sg_line_edit, test_dir, Qt.NoModifier)
        assert dialog.sg_line_edit.text() == test_dir

        def config_updated():
            assert self.config.saved_games_path == test_dir

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
                title='Select your {} directory'.format(dialog.config_settings['sg_path'].value_display_name),
                parent=dialog
            )

    def test_cancel(self, qtbot, random_line_edit_values):

        test_dir, test_file = random_line_edit_values

        qtbot.wait_until(lambda: self.dialog.btn_apply.isEnabled())
        qtbot.wait_until(lambda: self.dialog.btn_reset.isEnabled())

        qtbot.mouseClick(self.dialog.btn_cancel, Qt.LeftButton)

        qtbot.wait_until(lambda: not self.dialog.btn_apply.isEnabled())
        qtbot.wait_until(lambda: not self.dialog.btn_reset.isEnabled())
        qtbot.wait_until(lambda: not self.dialog.isVisible())

        assert self.config.saved_games_path == self.sg
        assert self.dialog.sg_line_edit.text() == test_dir
        assert self.config.cache_path == self.cache
        assert self.dialog.cache_line_edit.text() == test_dir
        assert self.config.kdiff_path == self.kdiff
        assert self.dialog.kdiff_line_edit.text() == test_file

    def test_ok(self, qtbot, random_line_edit_values):

        test_dir, test_file = random_line_edit_values

        qtbot.wait_until(lambda: self.dialog.btn_apply.isEnabled())
        qtbot.wait_until(lambda: self.dialog.btn_reset.isEnabled())

        qtbot.mouseClick(self.dialog.btn_ok, Qt.LeftButton)

        qtbot.wait_until(lambda: not self.dialog.btn_apply.isEnabled())
        qtbot.wait_until(lambda: not self.dialog.btn_reset.isEnabled())
        qtbot.wait_until(lambda: not self.dialog.isVisible())

        assert self.config.saved_games_path == test_dir
        assert self.dialog.sg_line_edit.text() == test_dir
        assert self.config.cache_path == test_dir
        assert self.dialog.cache_line_edit.text() == test_dir
        assert self.config.kdiff_path == test_file
        assert self.dialog.kdiff_line_edit.text() == test_file

    def test_reset(self, qtbot, random_line_edit_values):
        _, _ = random_line_edit_values

        qtbot.wait_until(lambda: self.dialog.btn_apply.isEnabled())
        qtbot.wait_until(lambda: self.dialog.btn_reset.isEnabled())

        qtbot.mouseClick(self.dialog.btn_reset, Qt.LeftButton)

        qtbot.wait_until(lambda: not self.dialog.btn_reset.isEnabled())
        qtbot.wait_until(lambda: not self.dialog.btn_apply.isEnabled())

        assert self.config.saved_games_path == self.sg
        assert self.dialog.sg_line_edit.text() == self.sg
        assert self.config.cache_path == self.cache
        assert self.dialog.cache_line_edit.text() == self.cache
        assert self.config.kdiff_path == self.kdiff
        assert self.dialog.kdiff_line_edit.text() == self.kdiff

    def test_directory_does_not_exist(self, qtbot, tmpdir, mocker):

        p = str(tmpdir.join('dir'))

        assert os.path.exists(p) is False

        save_settings = mocker.spy(self.dialog, 'save_settings')

        for qt_object, cfg_value, obj_name in {
            (self.dialog.sg_line_edit, self.sg, 'sg_path'),
            (self.dialog.cache_line_edit, self.cache, 'cache_path'),
        }:
            self.dialog.setup()

            show_error_balloon = mocker.spy(self.dialog.config_settings[obj_name], 'show_error_balloon')

            assert qt_object.text() == cfg_value

            qt_object.clear()
            qtbot.keyClicks(qt_object, p)
            qtbot.mouseClick(self.dialog.btn_apply, Qt.LeftButton)

            def settings_saved():
                save_settings.assert_called_with()

            qtbot.wait_until(settings_saved)

            show_error_balloon.assert_called_with('Directory does not exist')

    def test_not_a_directory(self, qtbot, tmpdir, mocker):

        p = tmpdir.join('dir')
        p.write('')
        p = str(p)

        assert os.path.exists(p) is True
        assert os.path.isfile(p) is True

        save_settings = mocker.spy(self.dialog, 'save_settings')

        for qt_object, cfg_value, obj_name in {
            (self.dialog.sg_line_edit, self.sg, 'sg_path'),
            (self.dialog.cache_line_edit, self.cache, 'cache_path'),
        }:
            self.dialog.setup()

            show_error_balloon = mocker.spy(self.dialog.config_settings[obj_name], 'show_error_balloon')

            assert qt_object.text() == cfg_value

            qt_object.clear()
            qtbot.keyClicks(qt_object, p)
            qtbot.mouseClick(self.dialog.btn_apply, Qt.LeftButton)

            def settings_saved():
                save_settings.assert_called_with()

            qtbot.wait_until(settings_saved)

            def show_error_called():
                show_error_balloon.assert_called_with('Not a directory')

            qtbot.wait_until(show_error_called)

    def test_check_for_update(self, qtbot, mocker):
        m = mocker.patch('src.ui.dialog_config.dialog.check_for_update')
        sig = mocker.patch('src.ui.dialog_config.dialog.SigMsg.show')
        qtbot.mouseClick(self.dialog.btn_update_check, Qt.LeftButton)
        qtbot.wait_until(m.assert_called_with)
        qtbot.wait_until(lambda: sig.assert_called_with(
            'Check done', 'Already running latest version of {}'.format(constants.APP_SHORT_NAME)))

    def test_kdiff_path_display_value(self):
        from src.ui.dialog_config.settings.setting_kdiff_path import KDiffPathSetting
        assert isinstance(self.dialog, ConfigDialog)
        assert isinstance(self.dialog.config_settings['kdiff_path'], KDiffPathSetting)
        assert isinstance(self.dialog.config_settings['kdiff_path'].value_display_name, str)

    def test_kdiff_download(self, mocker):
        from src.ui.dialog_config.settings.setting_kdiff_path import KDiffPathSetting
        assert isinstance(self.dialog, ConfigDialog)
        kdiff = self.dialog.config_settings['kdiff_path']
        assert isinstance(kdiff, KDiffPathSetting)
        m = mocker.patch('src.ui.dialog_config.settings.setting_kdiff_path.kdiff.download_and_install')
        assert m.call_count == 0
        kdiff.download_kdiff()
        m.assert_called_with(wait=False)
        m.reset()
        kdiff.q_action_install_kdiff.trigger()
        m.assert_called_with(wait=False)

    def test_kdiff_save_to_meta(self, mocker, config, tmpdir, somefile):
        from src.ui.dialog_config.settings.setting_kdiff_path import KDiffPathSetting
        assert isinstance(self.dialog, ConfigDialog)
        kdiff = self.dialog.config_settings['kdiff_path']
        assert isinstance(kdiff, KDiffPathSetting)
        assert kdiff.get_value_from_dialog() == self.kdiff

        validation_failed = mocker.spy(kdiff, 'validation_fail')
        validation_success = mocker.spy(kdiff, 'validation_success')
        show_error_balloon = mocker.spy(kdiff, 'show_error_balloon')

        kdiff.set_dialog_value('')
        assert kdiff.get_value_from_dialog() is None
        assert kdiff.save_to_meta() is True
        assert validation_failed.call_count == 0
        assert validation_success.call_count == 0
        assert show_error_balloon.call_count == 0
        kdiff.set_dialog_value('some_path')
        assert kdiff.save_to_meta() is False
        assert validation_failed.call_count == 1
        assert validation_success.call_count == 0
        show_error_balloon.assert_called_with('File does not exist')

        kdiff.set_dialog_value(somefile)
        assert kdiff.save_to_meta() is False
        show_error_balloon.assert_called_with('Expected a file named "kdiff3.exe"')
        assert validation_failed.call_count == 2
        assert validation_success.call_count == 0

        kdiff.set_dialog_value(str(tmpdir))
        assert kdiff.save_to_meta() is False
        show_error_balloon.assert_called_with('Not a file')
        assert validation_failed.call_count == 3
        assert validation_success.call_count == 0

        with mock.patch(
                'src.ui.dialog_config.settings.setting_kdiff_path.KDiffPathSetting.store_object',
                new=mock.PropertyMock(return_value=config)):
            p = str(tmpdir.join('kdiff3.exe'))
            with open(p, 'w') as f:
                f.write('')
            kdiff.set_dialog_value(p)
            assert kdiff.save_to_meta() is True
            assert show_error_balloon.call_count == 3
            assert validation_failed.call_count == 3
            assert validation_success.call_count == 2
            assert config.kdiff_path == p

    def test_kdiff_browse_for_value(self, mocker, somefile):
        from src.low.custom_path import Path
        m = mocker.patch('src.ui.dialog_config.settings.setting_kdiff_path.BrowseDialog.get_existing_file')
        m.return_value = Path(somefile)
        from src.ui.dialog_config.settings.setting_kdiff_path import KDiffPathSetting
        assert isinstance(self.dialog, ConfigDialog)
        kdiff = self.dialog.config_settings['kdiff_path']
        assert isinstance(kdiff, KDiffPathSetting)
        assert kdiff.get_value_from_dialog() == self.kdiff
        kdiff.browse_for_value()
        assert kdiff.get_value_from_dialog() == somefile
