# coding=utf-8

from hypothesis import strategies as st, given
from tests.init_qt_app import QtTestCase
from src.ui import MsgDialog


class TestDialogMsg(QtTestCase):

    @given(text=st.text(), title=st.text())
    def test_show(self, text, title):
        dialog = MsgDialog(text=text, title=title)
        dialog.show()
        self.assertTrue(dialog.qobj.isVisible())
        self.assertSequenceEqual(dialog.qobj.label.text(), text.replace('\n', '<br>'))
        self.assertSequenceEqual(dialog.qobj.windowTitle(), title)

    def test_adjust_size(self):
        base_text = 'some text'
        title = 'Title'
        for i in range(1, 40):
            text = '\n'.join([base_text] * i)
            dialog = MsgDialog(text=text, title=title)
            dialog.show()
            self.assertEqual(dialog.qobj.height(), 100 + (13 * max(len(text.split('\n')) - 3, 0)))
