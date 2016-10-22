# coding=utf-8

if __name__ == '__main__':
    import signal as core_sig

    from src import easi

    core_sig.signal(core_sig.SIGINT, easi.nice_exit)

    easi.start_gui()
