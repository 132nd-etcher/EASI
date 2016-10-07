# coding=utf-8

import time
from unittest import mock

from PyQt5.QtTest import QTest

from src.cfg import config
from src.low.custom_path import create_temp_file, create_temp_dir
from src.qt import Qt
from src.ui.dialog_config import ConfigDialog
from tests.init_qt_app import QtTestCase


class TestConfig(QtTestCase):
    def __init__(self, *args, **kwargs):
        QtTestCase.__init__(self, *args, **kwargs)
        self.dialog = ConfigDialog()

    def test_dialog(self):
        pass

    def test_subscribe_to_test_versions(self):
        pass

    def test_sg_path(self):
        test_dir = create_temp_dir()
        test_file = create_temp_file()
        test_no_exist = test_file.joinpath('xxx')
        config.saved_games_path = test_dir.abspath()
        self.assertIsNone(self.dialog.config_settings['sg_path'].value_default)
        self.assertIs(self.dialog.config_settings['sg_path'].value_type, str)
        self.dialog.show()
        self.dialog.load_settings()
        self.assertSequenceEqual(self.dialog.sg_line_edit.text(), test_dir.abspath())
        test_dir = create_temp_dir()
        self.dialog.sg_line_edit.clear()
        # noinspection PyArgumentList
        QTest.keyClicks(self.dialog.sg_line_edit, test_dir.abspath())
        self.assertSequenceEqual(self.dialog.sg_line_edit.text(), test_dir.abspath())
        QTest.mouseClick(self.dialog.buttonBox.button(self.dialog.buttonBox.Ok), Qt.LeftButton)
        time.sleep(0.1)
        self.assertSequenceEqual(config.saved_games_path, test_dir.abspath())
        self.dialog.show()
        self.dialog.sg_line_edit.clear()
        # noinspection PyArgumentList
        QTest.keyClicks(self.dialog.sg_line_edit, test_file.abspath())
        m = mock.MagicMock()
        self.dialog.config_settings['sg_path'].show_tooltip = m
        QTest.mouseClick(self.dialog.buttonBox.button(self.dialog.buttonBox.Ok), Qt.LeftButton)
        time.sleep(0.1)
        m.assert_called_with('Not a directory')
        self.assertSequenceEqual(config.saved_games_path, test_dir.abspath())
        self.dialog.show()
        self.dialog.sg_line_edit.clear()
        # noinspection PyArgumentList
        QTest.keyClicks(self.dialog.sg_line_edit, test_no_exist.abspath())
        m = mock.MagicMock()
        self.dialog.config_settings['sg_path'].show_tooltip = m
        QTest.mouseClick(self.dialog.buttonBox.button(self.dialog.buttonBox.Ok), Qt.LeftButton)
        time.sleep(0.1)
        m.assert_called_with('Directory does not exist')
        self.assertSequenceEqual(config.saved_games_path, test_dir.abspath())
        self.dialog.sg_line_edit.clear()
        self.dialog.sg_line_edit.setText('something')
        self.dialog.load_settings()
        self.assertSequenceEqual(config.saved_games_path, test_dir.abspath())
        with mock.patch('os.startfile') as m:
            self.dialog.config_settings['sg_path'].show_in_explorer()
            m.assert_called_with(test_dir.abspath())
        with mock.patch('src.ui.dialog_browse.dialog.BrowseDialog.get_directory') as m:
            self.dialog.config_settings['sg_path'].browse_for_dir()
            m.assert_called_with(
                init_dir=test_dir.abspath(),
                title='Select your {} directory'.format(self.dialog.config_settings['sg_path'].dir_name()),
                parent=self.dialog
            )
        self.dialog.sg_line_edit.setText(test_dir.abspath())
        self.dialog.accept()
