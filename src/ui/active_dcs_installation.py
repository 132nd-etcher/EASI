# coding=utf-8

import os

from src.cfg.cfg import Config
from src.dcs.dcs_installs import DCSInstalls, DCSInstall
from src.qt import QMenu, QAction
from src.ui.skeletons.main import Ui_MainWindow


class MainUiActiveDCSInstallation:
    def __init__(self, main_ui):
        assert isinstance(main_ui, Ui_MainWindow)
        self.main_ui = main_ui
        self.index = []
        self.menu = QMenu(self.main_ui)
        self.qact_show_main_install = QAction('Main installation', self.main_ui)
        self.qact_show_sg = QAction('Saved games', self.main_ui)

    def update_index(self):
        self.index = []
        dcs_installs = DCSInstalls()
        for dcs_install in dcs_installs:
            assert isinstance(dcs_install, DCSInstall)
            if dcs_install.install_path is not None:
                self.index.append(dcs_install)

    @property
    def btn(self):
        return self.main_ui.btn_active_dcs_installation_open_in_explorer

    @property
    def combo(self):
        return self.main_ui.combo_active_dcs_installation

    @property
    def active_dcs_installation(self) -> DCSInstall:
        idx = self.combo.currentIndex()
        return self.index[idx]

    def __show(self, attrib):
        try:
            os.startfile(getattr(self.active_dcs_installation, attrib))
        except FileNotFoundError:
            pass

    def open_active_install_in_explorer(self):
        self.__show('install_path')

    def open_active_sg_in_explorer(self):
        self.__show('saved_games')

    # noinspection PyUnresolvedReferences
    def setup(self):
        self.qact_show_main_install.setObjectName('show_main_install')
        self.qact_show_sg.setObjectName('show_sg')
        self.menu.addAction(self.qact_show_main_install)
        self.menu.addAction(self.qact_show_sg)
        self.btn.setMenu(self.menu)
        self.qact_show_main_install.triggered.connect(self.open_active_install_in_explorer)
        self.qact_show_sg.triggered.connect(self.open_active_sg_in_explorer)
        self.combo.currentIndexChanged.connect(self.current_index_changed)

    def current_index_changed(self):
        Config().active_dcs_installation = self.active_dcs_installation.label
        self.main_ui.label_dcs_version.setText(self.active_dcs_installation.version)

    def set_current_combo_index_to_config_value(self, value=None):
        if value is None:
            value = Config().active_dcs_installation
        if value is not None:
            dcs_install = DCSInstalls()[value]
            assert isinstance(dcs_install, DCSInstall)
            if dcs_install.install_path is not None:
                for idx, dcs_install in enumerate(self.index):
                    assert isinstance(dcs_install, DCSInstall)
                    if value == dcs_install.label:
                        self.combo.setCurrentIndex(idx)
                        return
        self.combo.setCurrentIndex(0)

    def known_dcs_installs_changed(self, value=None):
        self.combo.clear()
        self.update_index()
        for dcs_install in self.index:
            assert isinstance(dcs_install, DCSInstall)
            self.combo.addItem('({:6s}) {}'.format(
                dcs_install.label,
                dcs_install.install_path
            ))
        self.set_current_combo_index_to_config_value(value)

