# coding=utf-8
from src.keyring.keyring import keyring
from src.low.custom_logging import make_logger
from src.rem.db import DBSession
from src.sig import SignalReceiver, db_token_status_changed_sig
from src.ui.dialog_config.abstract_config_dialog_child import AbstractConfigDialogChild
from src.ui.skeletons.config_dialog import Ui_Settings

logger = make_logger(__name__)


class DBSettings(AbstractConfigDialogChild):
    def save_settings(self):
        return True

    def load_settings(self):
        pass

    def __init__(self, dialog: Ui_Settings):
        self.dialog = dialog
        self.dialog.btn_db_create.clicked.connect(self.db_start_auth_flow)
        self.dialog.btn_db_check_code.clicked.connect(self.db_finish_auth_flow)
        self.receiver = SignalReceiver(self)
        self.receiver[db_token_status_changed_sig] = self.db_token_status_changed
        self.flow = None

    def setup(self):
        pass

    def set_flow_elements_enabled(self, value: bool):
        self.dialog.label_db_validation_code_static.setEnabled(value)
        self.dialog.line_edit_db_validation_code.setEnabled(value)
        self.dialog.btn_db_check_code.setEnabled(value)

    def db_start_auth_flow(self):
        self.dialog.label_db_status.setText('Authenticating ...')
        self.dialog.label_db_status.setStyleSheet('QLabel {{ color : black; }}')
        self.set_flow_elements_enabled(True)
        self.flow = DBSession.start_auth_flow()

    def db_finish_auth_flow(self):
        if self.flow is None:
            return
        token = DBSession.finish_auth_flow(self.flow, self.dialog.line_edit_db_validation_code.text())
        self.dialog.line_edit_db_validation_code.clear()
        if token:
            keyring.db_token = token
            DBSession().authenticate(token)
            self.set_flow_elements_enabled(False)

    def db_token_status_changed(self, **kwargs):
        status = kwargs.get('status')
        if status == DBSession.session_status['not_connected']:
            self.dialog.label_db_status.setText('Not connected')
            self.dialog.label_db_status.setStyleSheet('QLabel { color : black; }')
        if status == DBSession.session_status['wrong_token']:
            self.dialog.label_db_status.setText('Token not accepted; please create a new one')
            self.dialog.label_db_status.setStyleSheet('QLabel { color : red; }')
        if status == DBSession.session_status['connected']:
            self.dialog.label_db_status.setText('Connected as: {}'.format(kwargs.get('username')))
            self.dialog.label_db_status.setStyleSheet('QLabel { color : green; }')
