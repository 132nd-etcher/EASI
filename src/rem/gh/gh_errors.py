# coding=utf-8
class GHSessionError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)


class RequestFailedError(GHSessionError):
    pass


class AuthenticationError(GHSessionError):
    pass


class RateLimitationError(GHSessionError):
    pass


class GithubAPIError(GHSessionError):
    pass


