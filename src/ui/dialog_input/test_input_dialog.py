# coding=utf-8

from tests.init_ui import get_qt_app

if __name__ == '__main__':
    get_qt_app()
    from src.ui.dialog_input.dialog import InputDialog

    inputs = [('label{}'.format(x), 'default{}'.format(x)) for x in range(15)]
    text = 'some long text\n' * 20
    print(
        InputDialog.make(
            text, 'title',
            inputs=inputs
        )
    )
    exit(0)
