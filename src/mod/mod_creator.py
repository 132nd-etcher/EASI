# coding=utf-8

from re import compile

import semver

from src.easi.ops import get_new_gh_login, confirm, select, warn, simple_input, get_dcs_version, long_input
from src.low import constants
from src.low import help_links
from src.low.custom_logging import make_logger
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.meta_repo.meta_repo import MetaRepo
from src.mod.mod_category import ModTypes
from src.mod.mod import Mod
from src.rem.gh.gh_session import GHSession
from src.sig import SIG_CREATE_NEW_MOD

logger = make_logger(__name__)
RE_MOD_NAME = compile(""".*[a-zA-Z]{4,}.*""")


class ModCreator():
    def __init__(self, meta_repo_name=None):
        self.__done = False
        self.__meta_repo_name = meta_repo_name
        self.__meta_repo = None
        self.__mod_name = None
        self.__mod_category = None
        self.__mod_version = None
        self.__dcs_version = None
        self.__mod_desc = ''
        self.__mod = None
        self.steps = [
            self._check_gh_login,
            self._select_metadata_repo,
            self._get_mod_name,
            self._select_mod_category,
            self._get_mod_version,
            self._get_dcs_version,
            self._get_desc,
            self._create_mod_object,
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

    @property
    def meta_repo(self):
        if not isinstance(self.__meta_repo, MetaRepo):
            raise ValueError('meta_repo should be initialized by now')
        return self.__meta_repo

    @property
    def mod(self):
        if not isinstance(self.__mod, Mod):
            raise ValueError('mod should be initialized by now')
        return self.__mod

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
            default=self.__meta_repo_name,
            help_link=help_links.mod_creation_meta_repo
        )
        if meta_repo_name is None:
            logger.debug('user cancelled')
            return False
        self.__meta_repo = LocalMetaRepo()[meta_repo_name]
        logger.debug('selected meta repo: {}'.format(meta_repo_name))
        return self._check_push_perm()

    def _check_push_perm(self):
        if not self.meta_repo.push_perm:
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
                        self.meta_repo.owner
                    ),
                    buttons='yesno'
            ):
                self._select_metadata_repo()
                return False
        return True

    def _get_mod_name(self):

        def verify_mod_name(_mod_name):
            if not self.meta_repo.mod_name_is_available_new(_mod_name):
                return 'There is already a mod named "{}" in repository "{}"'.format(_mod_name, self.__meta_repo.name)
            if not RE_MOD_NAME.match(_mod_name):
                return 'Mod name needs to contain at least one string of 4 letters'

        mod_name = simple_input(
            title='Choose a name for your mod',
            text='The name of your mod needs to contain at least 4 contiguous letters.\n\n'
                 'It also has to be unique in the current repository ({})'.format(self.meta_repo.name),
            verify_input_func=verify_mod_name,
            parent=constants.MAIN_UI,
            help_link=help_links.mod_creation_name
        )
        if mod_name:
            self.__mod_name = mod_name
            logger.debug('new mod name: {}'.format(mod_name))
            return True
        else:
            logger.debug('user cancelled')
            return False

    def _select_mod_category(self):
        logger.debug('selecting mod category')
        mod_category = select(
            choices=[x for x in ModTypes.category_names()],
            title='Select mod type',
            text='How would you describe your mod ?',
            help_link=help_links.mod_creation_type
        )
        if mod_category:
            logger.debug('mod category: {}'.format(mod_category))
            self.__mod_category = mod_category
            return True
        else:
            logger.debug('user cancelled')
            return False

    def _get_mod_version(self):

        def verify_version(version_str):
            try:
                semver.parse(version_str)
            except ValueError:
                return 'This is not a valid SemVer'

        mod_version = simple_input(
            title='Initial version',
            text='Choose an initial version number for your mod.\n\n',
            default='0.0.1',
            help_link=help_links.mod_creation_version,
            parent=constants.MAIN_UI
        )
        if mod_version:
            logger.debug('mod version: {}'.format(mod_version))
            self.__mod_version = mod_version
            return True
        else:
            logger.debug('user cancelled')
            return False

    def _get_dcs_version(self):
        dcs_version = get_dcs_version(
            title='DCS version',
            text='Select which version of DCS your mod is compatible with:',
            default='*',
            parent=constants.MAIN_UI,
        )
        if dcs_version:
            logger.debug('dcs version: {}'.format(dcs_version))
            self.__dcs_version = dcs_version
            return True
        else:
            logger.debug('user cancelled')
            return False

    def _get_desc(self):
        desc = long_input(
            title='Mod description',
            text='(optional)\n\nEnter a short description of your mod:',
            parent=constants.MAIN_UI
        )
        if desc:
            self.__mod_desc = desc
        return True

    def _create_mod_object(self):
        self.__mod = self.meta_repo.create_new_mod(self.__mod_name)
        self.mod.meta.category = self.__mod_category
        self.mod.meta.dcs_version = self.__dcs_version
        self.mod.meta.version = self.__mod_version
        self.mod.meta.description = self.__mod_desc
        self.mod.meta.write()



def init_mod_creator():
    logger.info('initializing')

    def on_sig_create_new_mod(sender, meta_repo_name):
        logger.debug('catched mod creation request from: {}'.format(sender))
        ModCreator(meta_repo_name=meta_repo_name)

    SIG_CREATE_NEW_MOD.connect(on_sig_create_new_mod, weak=False)

    logger.info('initializing')
