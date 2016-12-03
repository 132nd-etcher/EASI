# coding=utf-8


from src.qt import QPushButton, QBoxLayout, QSpacerItem, QSizePolicy
from src.ui.abstract.idyn_btns import IWithDynamicButtons


class WithDynamicButtons(IWithDynamicButtons):

    def __init__(self, btns_layout: QBoxLayout):
        self._dynbtns = {}
        self._btns_layout = btns_layout

    def btns_add_button(self, btn_text: str, btn_action: callable, start_enabled=True):
        self._dynbtns[btn_text] = (QPushButton(btn_text), start_enabled)
        self._btns_layout.addWidget(self._dynbtns[btn_text][0])
        self._dynbtns[btn_text][0].clicked.connect(btn_action)
        self._dynbtns[btn_text][0].setEnabled(start_enabled)

    def btns_set_enabled(self, value: bool):
        for btn in self._dynbtns.values():
            if btn[1] is False:
                btn[0].setEnabled(value)

    def btns_disconnect_all(self):
        self.btns_set_enabled(False)
        for btn in self._dynbtns.values():
            btn[0].clicked.disconnect()

    def btns_insert_space(self, spacer_size: int = 20):
        self._btns_layout.addSpacing(spacer_size)

    def btns_fill(self):
        spacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._btns_layout.addSpacerItem(spacer)

    def btns_get(self, btn_name) -> QPushButton:
        if btn_name in self._dynbtns:
            return self._dynbtns[btn_name][0]
        else:
            raise KeyError('no button named "{}"'.format(btn_name))
