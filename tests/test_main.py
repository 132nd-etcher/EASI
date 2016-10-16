# coding=utf-8

import sys
from src import main
import shutil


# @unittest.skipUnless(os.getenv('TEST_MAIN_LOOP') is not None, 'Not testing main loop')
def test_and_exit():
    sys.argv.append('test_and_exit')
    main.main()
    sys.argv.pop()
