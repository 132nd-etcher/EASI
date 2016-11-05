# coding=utf-8


from src.keyring.keyring import Keyring
from src.rem.gh.gh_session import GHAnonymousSession, GHSessionError
from src.sig import SIG_CREDENTIALS_GH_AUTH_STATUS


class GHCredentials:
    @staticmethod
    def remove():
        del Keyring().gh_username
        del Keyring().gh_password
        del Keyring().gh_token

    @staticmethod
    def authenticate(user, password):
        GHCredentials.remove()
        SIG_CREDENTIALS_GH_AUTH_STATUS.send(text='Authenticating ...', color='black')
        try:
            auth = GHAnonymousSession().create_new_authorization(user, password)
            token = auth.token
        except GHSessionError as e:
            if '401:' in e.msg:
                SIG_CREDENTIALS_GH_AUTH_STATUS.send(text='Wrong username / password', color='red')
            else:
                SIG_CREDENTIALS_GH_AUTH_STATUS.send(text=e.msg, color='red')
        else:
            if token:
                Keyring().gh_token = token
                Keyring().gh_username = user
                Keyring().gh_password = password
                SIG_CREDENTIALS_GH_AUTH_STATUS.send(text=user, color='green')
