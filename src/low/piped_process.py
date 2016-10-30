# coding=utf-8
"""
Runs a process in an external thread and logs the output to a standard Python logger
"""
import os
import subprocess
import threading

from utils.custom_logging import DEBUG


# noinspection PyPep8Naming
class _LogPipe(threading.Thread):
    def __init__(self, logger, level):
        """Setup the object with a logger and a loglevel
        and start the thread
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.level = level
        self.logger = logger
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe
        """
        return self.fdWrite

    def run(self):
        """Run the thread, logging everything.
        """
        for line in iter(self.pipeReader.readline, ''):
            # print(line.strip(os.linesep))
            self.logger.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        """Close the write end of the pipe.
        """
        os.close(self.fdWrite)


def run_piped_process(args, logger, level=DEBUG, cwd=None, env=None, exe=None):
    """
    Runs a standard process and pipes its output to a Python logger
    :param exe: path to executable (if None, will use first arg)
    :param env: dictionary with environment variables for the child process
    :param args: process and arguments ias a list
    :param logger: logger to send data to
    :param level: logging level, defaults to DEBUG
    :param cwd: working dir to spawn the process in (defaults to current)
    """
    log_pipe = _LogPipe(logger, level)

    logger.info('running: {} {} (in {})'.format(exe, ' '.join(args), cwd))
    with subprocess.Popen(args, stdout=log_pipe, stderr=log_pipe, cwd=cwd, env=env, executable=exe) as p:
        p.communicate()
        if p.returncode != 0:
            logger.error('return code: {}'.format(p.returncode))
            raise RuntimeError('command failed: {}'.format(args))
        log_pipe.close()
