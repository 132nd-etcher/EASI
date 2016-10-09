# coding=utf-8

from hypothesis import strategies as st, given

# noinspection PyProtectedMember
from src.ui.dialog_msg.dialog import _MsgDialog
from tests.utils import QtTestCase


class TestDialogMsg(QtTestCase):
    @given(text=st.text(), title=st.text())
    def test_show(self, text, title):
        dialog = _MsgDialog()
        dialog.show()
        dialog.label.setText(text.replace('\n', '<br>'))
        dialog.setWindowTitle(title)
        self.assertTrue(dialog.isVisible())
        self.assertSequenceEqual(dialog.label.text(), text.replace('\n', '<br>'))
        self.assertSequenceEqual(dialog.windowTitle(), title)

    def test_adjust_size(self):
        base_text = 'some text'
        title = 'Title'
        for i in range(1, 40):
            text = '\n'.join([base_text] * i)
            dialog = _MsgDialog()
            dialog.label.setText(text)
            dialog.setWindowTitle(title)
            dialog.show()
            self.assertGreaterEqual(dialog.height(), 100 + (13 * max(len(text.split('\n')) - 3, 0)) - (3 * i))
