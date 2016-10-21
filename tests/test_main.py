# coding=utf-8

import sys


def test_and_exit():
    sys.argv.append('test_and_exit')
    from src import main
    main.main()
    sys.argv.pop()
