# coding=utf-8

import sys

from src import main


def test_and_exit():
    sys.argv.append('test_and_exit')
    main.main()
    sys.argv.pop()
