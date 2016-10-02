# coding=utf-8

from tests.init_ui import get_qt_app

if __name__ == '__main__':
    qt_app, main_ui = get_qt_app()
    import time
    from src.sig import sig_long_op_dialog

    sig_long_op_dialog.show(title='title', text='some text')


    def dummy_update():
        for i in range(0, 101, 10):
            sig_long_op_dialog.set_progress(value=i)
            time.sleep(0.5)


    from src.threadpool import ThreadPool

    pool = ThreadPool(1, 'test', True)
    pool.queue_task(dummy_update)
    exit(qt_app.exec())
