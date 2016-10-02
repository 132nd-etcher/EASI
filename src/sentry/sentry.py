# coding=utf-8

import certifi
import sys
import types

import raven.breadcrumbs

from src.__version__ import __version__
from src.abstract import SentryContextInterface
from src.low import constants
from src.low.custom_logging import make_logger

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret

logger = make_logger(__name__)

registered = {}


def sentry_register_context(key, obj):
    """Registers a context to be read when a crash occurs; obj must implement get_context()"""
    global registered
    registered[key] = obj


def filter_breadcrumbs(_logger, level, msg, *args, **kwargs):
    if _logger == 'requests':
        return False
    return True


raven.breadcrumbs.register_special_log_handler('__main__', filter_breadcrumbs)

if Secret.sentry_dsn is None:
    raise Exception('fuckit')

if Secret.sentry_dsn is not None:  # and not constants.TESTING:
    crash_reporter = raven.Client(
        'https://{}@sentry.io/99772?ca_certs={}'.format(Secret.sentry_dsn, certifi.where()),
        release=__version__
    )
else:
    crash_reporter = raven.Client()

try:
    crash_reporter.tags_context(
        {
            'frozen'         : constants.FROZEN,
            'platform'       : sys.platform,
            'windows_version': sys.getwindowsversion(),
        }
    )
except AttributeError:
    crash_reporter.tags_context(
        {
            'frozen'  : constants.FROZEN,
            'platform': sys.platform,
        }
    )

# ---------------------------------------------------------------------------------------------------------------------
# Overloads captureException
# ----------------------------------------------------
old_capture_exc = crash_reporter.captureException


def capture_with_context(_, exc_info=None, **kwargs):
    logger.debug('capturing exception')
    for k in registered:
        context_provider = registered[k]
        assert isinstance(context_provider, SentryContextInterface)
        crash_reporter.extra_context({k: context_provider.get_context()})
    old_capture_exc(exc_info, **kwargs)


# crash_reporter.captureException = capture_with_context
crash_reporter.captureException = types.MethodType(capture_with_context, crash_reporter)

# ---------------------------------------------------------------------------------------------------------------------
# Overloads the send method in script mode
# ----------------------------------------------------
if not constants.FROZEN:
    def dummy_capture(*args, **kwargs):
        logger.error('crash report would have been sent')
        # logger.error(pprint.pformat(data))


    crash_reporter.captureException = types.MethodType(dummy_capture, crash_reporter)
# ----------------------------------------------------
