# coding=utf-8

from src.cfg.cfg import Config
from src.sentry.sentry import crash_reporter
from src.sig import SigMsg


def send_feedback(msg: str, msg_type: str):
    crash_reporter.extra_context(
        data={
            'user': Config().usr_name,
            'mail': Config().usr_email,
        }
    )
    text = '{}\n{}'.format(msg_type, msg)
    crash_reporter.captureMessage(
        message=text, level='debug',
        tags={
            'message': msg_type,
            'type': 'message',
        }
    )
    SigMsg().show('Thank you', 'Thank you for your feedback !')
