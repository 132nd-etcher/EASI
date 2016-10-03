# coding=utf-8

import github3
import requests

from src.low import constants
from src.low.custom_logging import make_logger

logger = make_logger(__name__)


class TokenRequestError(Exception):

    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        super(TokenRequestError, self).__init__(msg,  *args, **kwargs)


def gh_request_token(username: str, password: str) -> str or None:
    auth = (username, password)

    def _search_for_existing_token():
        logger.debug('searching for existing token')
        _req = requests.get('https://api.github.com/authorizations', auth=auth)
        j = _req.json()
        auth_id = None
        for x in j:
            if x['app']['name'] == constants.APP_SHORT_NAME:
                auth_id = x['id']
        return auth_id

    def _remove_existing_token(token_id):
        return requests.delete('https://api.github.com/authorizations/{}'.format(token_id), auth=auth)

    logger.debug('logging in to Github')
    try:
        g = github3.login(username, password)
        rate_limit = g.ratelimit_remaining
        if rate_limit < 500:
            print('rate limit is getting low')  # TODO
        logger.debug('rate limit remaining: {}'.format(rate_limit))
        existing_token_id = _search_for_existing_token()
        if existing_token_id:
            logger.debug('token for {} exists, removing'.format(constants.APP_SHORT_NAME))
            req = _remove_existing_token(existing_token_id)
            if req.status_code != 204:
                raise TokenRequestError('removal of existing token for {} failed'.format(constants.APP_SHORT_NAME))
        logger.debug('getting a new token')
        auth = github3.authorize(login=username, password=password, scopes=['user', 'repo', 'delete_repo'],
                                 note=constants.APP_SHORT_NAME)
        return auth.token
    except github3.GitHubError as e:
        if e.code == 401:
            raise TokenRequestError('wrong username/password')
        elif e.code == 403:
            raise TokenRequestError('too many failed attempts')
        else:
            logger.exception('login failed')
            raise
