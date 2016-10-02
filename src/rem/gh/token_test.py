# coding=utf-8

import github3


def gh_token_is_valid(token: str) -> bool:
    g = github3.login(token=token)
    try:
        # noinspection PyStatementEffect
        usr = g.user()
        return usr.name
    except github3.GitHubError:
        return False
