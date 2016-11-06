# coding=utf-8
import src.easi.nice_exit

if __name__ == '__main__':
    import signal as core_sig

    from src.easi import easi

    core_sig.signal(core_sig.SIGINT, src.easi.nice_exit.nice_exit)

    easi.start_gui()
