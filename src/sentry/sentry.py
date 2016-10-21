# coding=utf-8

import logging
import sys

import certifi
import raven.breadcrumbs

from src.__version__ import __version__
from src.abstract.abstract_sentry import SentryContextInterface
from src.cfg import Config
from src.rem.gh.gh_session import GHSession
from src.low import constants
from src.low.custom_logging import make_logger

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret

logger = make_logger(__name__)


class Sentry(raven.Client):
    def __init__(self):
        self.registered_contexts = {}
        if Secret.sentry_dsn is not None:  # and not constants.TESTING:
            raven.Client.__init__(
                self,
                'https://{}@sentry.io/99772?ca_certs={}'.format(Secret.sentry_dsn, certifi.where()),
                release=__version__
            )
        else:
            raven.Client.__init__(self)

    def set_context(self):
        self.tags_context(
            dict(
                frozen=constants.FROZEN,
                platform=sys.platform,
                release_name=constants.APP_RELEASE_NAME,
                testing=constants.TESTING,
            )
        )
        if Config().usr_name:
            self.tags_context(dict(username=Config().usr_name))
        if Config().usr_email:
            self.tags_context(dict(user_email=Config().usr_email))
        if GHSession().user:
            self.tags_context(dict(gh_username=GHSession().user.login))
        try:
            self.tags_context(dict(windows_version=sys.getwindowsversion()))
        except AttributeError:
            pass

    def register_context(self, key, obj):
        """Registers a context to be read when a crash occurs; obj must implement get_context()"""
        self.registered_contexts[key] = obj

    def captureMessage(self, message, **kwargs):
        self.set_context()
        if kwargs.get('data') is None:
            kwargs['data'] = {}
        if kwargs['data'].get('level') is None:
            kwargs['data']['level'] = logging.DEBUG
        for k, context_provider in self.registered_contexts.items():
            assert isinstance(context_provider, SentryContextInterface)
            crash_reporter.extra_context({k: context_provider.get_context()})
        super(Sentry, self).captureMessage(message, **kwargs)

    def captureException(self, exc_info=None, **kwargs):
        self.set_context()
        if not constants.FROZEN:
            logger.error('crash report would have been sent')
            return

        logger.debug('capturing exception')
        for k, context_provider in self.registered_contexts.items():
            assert isinstance(context_provider, SentryContextInterface)
            crash_reporter.extra_context({k: context_provider.get_context()})
        super(Sentry, self).captureException(exc_info, **kwargs)


crash_reporter = Sentry()


# noinspection PyUnusedLocal
def filter_breadcrumbs(_logger, level, msg, *args, **kwargs):
    skip_lvl = []
    skip_msg = []

    if level in skip_lvl or msg in skip_msg:
        return False

    # print('got args, kwargs: ', args, kwargs)
    if _logger == 'requests':
        return False
    return True


raven.breadcrumbs.register_special_log_handler('__main__', filter_breadcrumbs)
