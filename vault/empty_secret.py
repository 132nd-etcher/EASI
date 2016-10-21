# coding=utf-8

"""
To enable sentry, place a "secret.py" file in the "vault" directory with the following structure
"""


class Secret:
    sentry_dsn = None
    gh_client_id = None
    gh_client_secret = None
    db_app_key = None
    db_app_secret = None
    gh_test_token = None
    gh_test_login = None
    gh_test_usermail = None
    bt_token = None
