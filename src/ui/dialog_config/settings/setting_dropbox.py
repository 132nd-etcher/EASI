# coding=utf-8
from src.qt import QLabel
from blinker_herald import signals
from src.rem.db.db_session import DBSession
from src.ui.dialog_config.settings.abstract_credential import AbstractCredentialSetting


class DropboxSetting(AbstractCredentialSetting):
    def __init__(self, dialog):
        AbstractCredentialSetting.__init__(self, dialog)
        self.flow = None

        @signals.post_authenticate.connect_via('DBSession', weak=False, )
        def status_changed(_, **kwargs):
            self.status_changed(kwargs['result'])

    def status_changed(self, result):
        super(DropboxSetting, self).status_changed(result)

    @property
    def qt_object(self):
        return self.dialog.btn_db_check_code

    @property
    def value_name(self) -> str:
        return 'db_token'

    def set_flow_elements_enabled(self, value: bool):
        self.dialog.label_db_validation_code_static.setEnabled(value)
        self.dialog.line_edit_db_validation_code.setEnabled(value)
        self.dialog.btn_db_check_code.setEnabled(value)

    def setup(self):
        self.dialog.btn_db_check_code.clicked.connect(self.check_code)
        self.set_flow_elements_enabled(False)

    def check_code(self):
        if self.flow is None:
            return
        token = DBSession.finish_auth_flow(self.flow, self.dialog.line_edit_db_validation_code.text())
        self.dialog.line_edit_db_validation_code.clear()
        if token:
            DBSession().authenticate(token)
            self.save_to_meta(token)
            self.set_flow_elements_enabled(False)

    @property
    def auth_btn(self):
        return self.dialog.btn_db_create

    def authenticate(self):
        self.status_label.setText('Authenticating ...')
        self.status_label.setStyleSheet('QLabel {{ color : black; }}')
        self.set_flow_elements_enabled(True)
        self.flow = DBSession.start_auth_flow()

    @property
    def session_object(self):
        return DBSession

    @property
    def status_label(self) -> QLabel:
        return self.dialog.label_db_status
