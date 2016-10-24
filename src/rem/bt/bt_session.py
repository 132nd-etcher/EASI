# coding=utf-8

import requests
from requests.sessions import Session

from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.rem.bt.bt_objects.bt_file import BTAllFiles
from src.rem.bt.bt_objects.bt_version import BTVersion, BTAllVersions

logger = make_logger(__name__)


try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret


class BTSessionError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)


class BTNotFoundError(BTSessionError):
    pass


class RequestFailedError(BTSessionError):
    pass


class AuthenticationError(BTSessionError):
    pass


class RateLimitationError(BTSessionError):
    pass


class BintrayAPIError(BTSessionError):
    pass


class BTSession(Session, metaclass=Singleton):
    def __init__(self):
        Session.__init__(self)
        self.base = ['https://api.bintray.com']
        self.subject = '132nd-etcher'
        self.repo = 'EASI'
        self.__resp = None
        self.req = None

    @property
    def resp(self) -> requests.models.Response:
        return self.__resp

    def build_req(self, *args):
        if not args:
            raise ValueError('request is empty')
        for x in args:
            if not isinstance(x, str):
                raise TypeError('expected a string, got: {} ({})'.format(x, args))
        self.req = '/'.join(self.base + list(args))
        return self.req

    def __parse_resp_error(self):
        logger.error(self.req)
        if self.resp.status_code >= 500:
            raise BintrayAPIError(r'Bintray API seems to be down, check https://http://status.bintray.com/')
        else:
            code = self.resp.status_code
            reason = self.resp.reason
            msg = [str(code), reason]
            json = self.resp.json()
            if json:
                msg.append('BT_MSG: {}'.format(json.get('message')))
                msg.append('BT_DOC: {}'.format(json.get('documentation_url')))
                if code == 403:
                    raise RateLimitationError(': '.join(msg))
            if code == 401:
                raise AuthenticationError(': '.join(msg))
            if code == 404:
                raise BTNotFoundError(self.req)
            else:
                raise BTSessionError(': '.join(msg))

    def __parse_resp(self) -> requests.models.Response:
        if self.__resp is None:
            raise RequestFailedError('did not get any response from: {}'.format(self.req))
        if not self.__resp.ok:
            self.__parse_resp_error()
        logger.debug(self.__resp.reason)
        return self.__resp

    def _get(self, **kwargs) -> requests.models.Response:
        logger.debug(self.req)
        self.__resp = super(BTSession, self).get(self.req, **kwargs)
        return self.__parse_resp()

    def _get_json(self, **kwargs) -> requests.models.Response:
        req = self._get(**kwargs)
        return req.json()

    def get_files_for_package(self, package) -> BTAllFiles:
        self.build_req('packages', self.subject, self.repo, package, 'files')
        return BTAllFiles(self._get_json())

    def get_version(self, package, version) -> BTAllVersions:
        self.build_req('packages', self.subject, self.repo, package, 'versions', version)
        return BTAllVersions(self._get_json())

    def get_latest_version(self, package) -> BTVersion:
        self.build_req('packages', self.subject, self.repo, package, 'versions', '_latest')
        return BTVersion(self._get_json())


bt_session = BTSession()
