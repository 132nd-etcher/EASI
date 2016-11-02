# coding=utf-8

import pygit2
from pygit2 import Signature

from src.keyring.keyring import Keyring
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from src.rem.gh.gh_session import GHSession

logger = make_logger(__name__)


class Repository:
    repo_status_map = {
        pygit2.GIT_STATUS_CONFLICTED: 'conflicted',
        pygit2.GIT_STATUS_CURRENT: 'current',
        pygit2.GIT_STATUS_IGNORED: 'ignored',
        pygit2.GIT_STATUS_INDEX_DELETED: 'index deleted',
        pygit2.GIT_STATUS_INDEX_MODIFIED: 'index modified',
        pygit2.GIT_STATUS_INDEX_NEW: 'index new',
        pygit2.GIT_STATUS_WT_DELETED: 'working tree deleted',
        pygit2.GIT_STATUS_WT_NEW: 'working tree new',
        pygit2.GIT_STATUS_WT_MODIFIED: 'working tree modified',
    }

    def __init__(self, path: str or Path, auto_init=True):
        if isinstance(path, str):
            path = Path(path)
        self.__path = path
        self.debug('creating Repository object')
        if self.is_init:
            self.__repo = pygit2.Repository(str(self.path.joinpath('.git').abspath()))
        elif auto_init:
            self.__repo = self.init()

    def debug(self, text):
        logger.debug('{}: {}'.format(self.path.abspath(), text))

    def info(self, text):
        logger.debug('{}: {}'.format(self.path.abspath(), text))

    def warning(self, text):
        logger.debug('{}: {}'.format(self.path.abspath(), text))

    def error(self, text):
        logger.debug('{}: {}'.format(self.path.abspath(), text))

    @property
    def repo(self) -> pygit2.Repository:
        return self.__repo

    @property
    def path(self):
        return self.__path

    @property
    def is_init(self):
        return self.path.joinpath('.git').exists()

    @property
    def status(self):
        return {k: self.repo_status_map[v] for k, v in self.repo.status().items()}

    def filter_status(self, status):
        for file, file_status in self.status.items():
            if file_status == status:
                yield file

    @property
    def working_dir_new(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_WT_NEW])

    @property
    def working_dir_modified(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_WT_MODIFIED])

    @property
    def working_dir_deleted(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_WT_DELETED])

    @property
    def index_new(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_INDEX_NEW])

    @property
    def index_modified(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_INDEX_MODIFIED])

    @property
    def index_deleted(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_INDEX_DELETED])

    @property
    def current(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_CURRENT])

    @property
    def ignored(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_IGNORED])

    @property
    def conflicts(self):
        return self.filter_status(self.repo_status_map[pygit2.GIT_STATUS_CONFLICTED])

    @property
    def is_clean(self):
        return len(self.status) == 0

    def add(self, file):
        path = Path(file)
        self.debug('adding: {}'.format(path.abspath()))
        index = self.repo.index
        index.add(path.relpath(self.path.abspath()))
        index.write()

    def remove(self, file):
        path = Path(file)
        self.debug('adding: {}'.format(path.abspath()))
        index = self.repo.index
        index.remove(path.relpath(self.path.abspath()))
        index.write()

    def commit(self, msg: str, author: str = None, author_mail: str = None, add_all=False):
        if GHSession().user is not None:
            if author is None:
                author = GHSession().user.login
            if author_mail is None:
                author_mail = GHSession().primary_email.email
        else:  # FIXME use those provided in git config
            if author is None:
                raise ValueError('no author given')
            if author_mail is None:
                raise ValueError('no author mail given')
        sig = Signature(author, author_mail)
        author, committer = sig, sig
        index = self.repo.index
        if add_all:
            index.add_all()
            index.write()
        tree = index.write_tree()
        self.repo.create_commit(self.repo.head.name, author, committer, msg, tree, [self.repo.head.get_object().hex])

    def hard_reset(self):
        self.repo.reset(self.head.target, pygit2.GIT_RESET_HARD)

    @property
    def head(self):
        return self.repo.head

    def walk(self, oid, sort_mode=pygit2.GIT_SORT_TIME):
        return self.repo.walk(oid, sort_mode)

    @staticmethod
    def clone(url, path, bare=False, repository=None, remote=None, checkout_branch='master', callbacks=None):
        logger.debug('cloning "{}" into "{}"'.format(url, path))
        repo = pygit2.clone_repository(url, path, bare, repository, remote, checkout_branch, callbacks or Callbacks())
        return repo

    def init(self):
        if self.is_init:
            raise FileExistsError('repository already initialized')
        pygit2.init_repository(str(self.path.abspath()))
        repo = pygit2.Repository(str(self.path.joinpath('.git').abspath()))
        if GHSession().user is not None:
            sig = Signature(GHSession().user.login, GHSession().primary_email.email)
        else:
            sig = Signature('EASI', 'EASI@EASI.com')
        author, committer = sig, sig
        index = repo.index
        tree = index.write_tree()
        repo.create_commit('refs/heads/master', author, committer, 'EASI: initial commit', tree, [])
        return repo

    @property
    def remotes(self):
        return self.repo.remotes

    def pull(self, remote_name='origin'):
        for remote in self.remotes:
            if remote.name == remote_name:
                remote.fetch()
                remote_master_id = self.repo.lookup_reference('refs/remotes/origin/master').target
                merge_result, _ = self.repo.merge_analysis(remote_master_id)
                # Up to date, do nothing
                if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                    print('repository already up-to-date')
                    return
                # We can just fastforward
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                    print('fast-forward to origin/master')
                    self.repo.checkout_tree(self.repo.get(remote_master_id))
                    master_ref = self.repo.lookup_reference('refs/heads/master')
                    master_ref.set_target(remote_master_id)
                    self.repo.head.set_target(remote_master_id)
                # Need to check for conflicts
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
                    print('merging origin/master')
                    self.repo.merge(remote_master_id)
                    print(self.repo.index.conflicts)

                    assert self.repo.index.conflicts is None, 'Conflicts, ahhhh!'
                    user = self.repo.default_signature
                    tree = self.repo.index.write_tree()
                    commit = self.repo.create_commit('HEAD',
                                                     user,
                                                     user,
                                                     'auto-merge from origin',
                                                     tree,
                                                     [self.repo.head.target, remote_master_id])
                    self.repo.state_cleanup()
                else:
                    raise AssertionError('Unknown merge analysis result')


class Callbacks(pygit2.RemoteCallbacks):
    def certificate_check(self, certificate, valid, host):
        print(host)
        return True

    def transfer_progress(self, stats):
        print(stats)

    def sideband_progress(self, string):
        print(string)

    def push_update_reference(self, ref_name, message):
        print(ref_name)
        print(message)

    def credentials(self, url, username_from_url, allowed_types):
        return pygit2.UserPass(Keyring().gh_username, Keyring().gh_password)
