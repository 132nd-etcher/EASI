# coding=utf-8

# coding=utf-8

from src.ui.dialog_config.settings.abstract_config import AbstractConfigSetting


class ExperimentalUpdateSetting(AbstractConfigSetting):

    @property
    def qt_object(self):
        return self.dialog.subscribe_to_test_versions

    def dialog_has_changed_methods(self) -> list:
        return [self.dialog.subscribe_to_test_versions.clicked]

    def setup(self):
        pass

    def get_value_from_dialog(self):
        return self.dialog.subscribe_to_test_versions.isChecked()

    def validate_dialog_value(self) -> bool:
        return True

    def set_dialog_value(self, value):
        self.dialog.subscribe_to_test_versions.setChecked(self.value)
