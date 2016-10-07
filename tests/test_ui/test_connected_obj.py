# coding=utf-8

from unittest import TestCase, mock


class TestConnectedObject(TestCase):
    # noinspection PyClassHasNoInit
    def test_connected_object(self):
        from src.sig import CustomSignal
        from src.abstract.ui.connected_object import AbstractConnectedObject

        sig = CustomSignal()

        class C(AbstractConnectedObject):
            pass

        from src.ui.main_ui.main_ui import MainUi
        import src.abstract.ui.connected_object
        src.abstract.ui.connected_object.main_ui = None
        with self.assertRaises(RuntimeError):
            C(sig, 'some_obj')
        with mock.patch('src.abstract.ui.connected_object.main_ui', spec=MainUi) as m:
            m.some_obj = mock.MagicMock()
            m.sig_proc = mock.MagicMock()
            m.sig_proc.do = mock.MagicMock()
            c = C(sig, 'some_obj')
            c.some_func = mock.MagicMock()
            sig.send(op='some_func')
            m.sig_proc.do.assert_called_with('some_obj', 'some_func')
            with self.assertRaises(AttributeError):
                sig.send(op='missing op')
            with self.assertRaises(AttributeError):
                C(sig, 'missing_obj')
                sig.send(op='some_func')
            with self.assertRaises(TypeError):
                C('not_a_sig', 'some_obj')
                sig.send(op='some_func')
