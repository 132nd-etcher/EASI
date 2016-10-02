# coding=utf-8

from tests.init_ui import get_qt_app

if __name__ == '__main__':
    qt_app, main_ui = get_qt_app()
    import time

    from src.threadpool import ThreadPool
    from src.sig import sig_long_op_dual_dialog

    sig_long_op_dual_dialog.show('title', 'some text')


    def dummy_update():
        for i in range(10, 101, 10):
            for y in range(10, 101, 10):
                sig_long_op_dual_dialog.set_current_text(y)
                sig_long_op_dual_dialog.set_current_progress(y)
                time.sleep(0.1)
            sig_long_op_dual_dialog.set_progress(i)
            sig_long_op_dual_dialog.set_text(i)


    pool = ThreadPool(1, 'test', True)
    pool.queue_task(dummy_update)
    exit(qt_app.exec())
