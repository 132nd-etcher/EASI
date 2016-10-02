# coding=utf-8

import os

from src.cfg import config
from src.dcs import dcs_installs
from src.qt import *
from src.sig import SignalReceiver, sig_dcs_installs_changed
from src.ui.skeletons.main import Ui_MainWindow


class MainUiActiveDCSInstallation:
    def __init__(self, main_ui):
        assert isinstance(main_ui, Ui_MainWindow)
        self.main_ui = main_ui
        self.index = []
        self.config_mapping = {}
        self.receiver = SignalReceiver(self)
        self.receiver[sig_dcs_installs_changed] = self.dcs_installs_changed

    def update_index(self):
        self.index = []
        for x, y in [
            (dcs_installs.stable, 'stable'),
            (dcs_installs.beta, 'beta'),
            (dcs_installs.alpha, 'alpha'),
        ]:
            if x[0] is not None:
                self.index.append((x, y))
        self.config_mapping = {
            'stable': dcs_installs.stable,
            'beta'  : dcs_installs.beta,
            'alpha' : dcs_installs.alpha,
        }

    @property
    def btn(self):
        return self.main_ui.btn_active_dcs_installation_open_in_explorer

    @property
    def combo(self):
        return self.main_ui.combo_active_dcs_installation

    @property
    def active_dcs_installation(self):
        idx = self.combo.currentIndex()
        return self.index[idx]

    def show_main_install(self):
        try:
            os.startfile(self.active_dcs_installation[0][0].abspath())
        except FileNotFoundError:
            pass

    def show_main_sg(self):
        try:
            os.startfile(self.active_dcs_installation[0][1].abspath())
        except FileNotFoundError:
            pass

    def setup(self):
        self.menu = QMenu(self.main_ui)
        self.qact_show_main_install = QAction('Main installation', self.main_ui)
        self.qact_show_sg = QAction('Saved games', self.main_ui)
        self.qact_show_main_install.setObjectName('show_main_install')
        self.qact_show_sg.setObjectName('show_sg')
        self.menu.addAction(self.qact_show_main_install)
        self.menu.addAction(self.qact_show_sg)
        self.btn.setMenu(self.menu)
        self.connect_qactions()
        self.combo.currentIndexChanged.connect(self.current_index_changed)

    def current_index_changed(self):
        config.active_dcs_installation = self.active_dcs_installation[1]
        self.main_ui.label_dcs_version.setText(self.active_dcs_installation[0][2])

    # noinspection PyUnresolvedReferences
    def connect_qactions(self):
        self.qact_show_main_install.triggered.connect(self.show_main_install)
        self.qact_show_sg.triggered.connect(self.show_main_sg)

    def set_current_combo_index_to_config_value(self):
        if config.active_dcs_installation is not None:
            dcs_install = self.config_mapping[config.active_dcs_installation]
            if dcs_install[0] is not None:
                for idx, x in enumerate(self.index):
                    if config.active_dcs_installation == x[1]:
                        self.combo.setCurrentIndex(idx)
                        return
        self.combo.setCurrentIndex(0)

    def dcs_installs_changed(self, **kwargs):
        self.combo.clear()
        self.update_index()
        for x in self.index:
            self.combo.addItem('({:6s}) {}'.format(x[1], x[0][0].abspath()))
        self.set_current_combo_index_to_config_value()
