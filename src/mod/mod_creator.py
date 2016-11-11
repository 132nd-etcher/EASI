# coding=utf-8

from re import compile

from src.easi.ops import get_new_gh_login, confirm, select, warn, simple_input
from src.low import constants
from src.low.custom_logging import make_logger
from src.low.singleton import Singleton
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.meta_repo.meta_repo import MetaRepo
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_CREATE_NEW_MOD

logger = make_logger(__name__)
RE_MOD_NAME = compile(""".*[a-zA-Z]{4,}.*""")


class ModCreator(metaclass=Singleton):
    def __init__(self):
        self.__done = False
        self.__meta_repo = None
        self.__mod_name = None
        self.steps = [
            self._check_gh_login,
            self._select_metadata_repo,
            self._get_mod_name,
        ]
        while True:
            try:
                step = self.steps.pop(0)
                logger.debug('next step: '.format(step.__name__))
                if not step():
                    break
            except IndexError:
                self.__done = True
                break
        if not self.__done:
            logger.debug('mod creation failed')
        else:
            logger.debug('mod creation successful')

    def _check_gh_login(self):
        logger.debug('checking GH login')
        if not GHSession().has_valid_token:
            logger.debug('no valid token, asking user for one')
            return self._get_gh_token()
        return True

    def _get_gh_token(self):
        if confirm('Creating a mod requires a valid Github account.<br><br>'
                   'Would you like to connect your Github account now?',
                   'Github account not connected'):
            if not get_new_gh_login(constants.MAIN_UI):
                logger.debug('still no valid token')
                return False
        else:
            logger.debug('user declined')
            return False
        return True

    def _select_metadata_repo(self):
        logger.debug('prompting for meta repo')
        choices = [
            LocalMetaRepo().own_meta_repo.name,
            LocalMetaRepo().root_meta_repo.name,
        ]
        for meta_repo_name in LocalMetaRepo().names:
            if meta_repo_name not in choices:
                choices.append(meta_repo_name)
        meta_repo_name = select(
            choices=choices,
            title='Select a meta repository',
            text='Select which metadata repository you want to use to host your mod.',
            help_link=r'https://132nd-etcher.github.io/EASI/mod_creation/#step-1-select-a-repository',
        )
        if meta_repo_name is None:
            logger.debug('user cancelled')
            return False
        self.__meta_repo = LocalMetaRepo()[meta_repo_name]
        logger.debug('selected meta repo: {}'.format(meta_repo_name))
        return self._check_push_perm()

    def _check_push_perm(self):
        if not self.__meta_repo.push_perm:
            if not warn(
                    'nopushperm',
                    'You are about to create a mod in a repository in which you do not have push permission '
                    '(i.e. you cannot write directly to it).\n\n'
                    ''
                    'Your changes will instead be sent as a "Pull Request" (an update proposal) '
                    'the the repository owner ({})\n\n'
                    ''
                    'Make sure you understand the implications before going further'
                    ''
                    'Do you want to continue?'.format(
                        self.__meta_repo.owner
                    ),
                    buttons='yesno'
            ):
                self._select_metadata_repo()
                return False
        return True

    def _get_mod_name(self):

        def verify_mod_name(_mod_name):
            assert isinstance(self.__meta_repo, MetaRepo)
            if not self.__meta_repo.mod_name_is_available_new(_mod_name):
                return 'There is already a mod named "{}" in repository "{}"'.format(_mod_name, self.__meta_repo.name)
            if not RE_MOD_NAME.match(_mod_name):
                return 'Mod name needs to contain at least one string of 4 letters'

        mod_name = simple_input(
            title='Choose a name for your mod',
            text='The name of your mod needs to contain at least 4 contiguous letters.\n\n'
                 'It also has to be unique in the current repository ({})'.format(self.__meta_repo.name),
            verify_input_func=verify_mod_name,
            parent=constants.MAIN_UI,
            # help_link= FIXME
        )
        if mod_name:
            self.__mod_name = mod_name
            logger.debug('new mod name: {}'.format(mod_name))
            return True
        else:
            logger.debug('user cancelled')
            return False


def on_sig_create_new_mod(sender):
    logger.debug('catched mod creation request from: {}'.format(sender))
    ModCreator()


SIG_CREATE_NEW_MOD.connect(on_sig_create_new_mod, weak=False)
