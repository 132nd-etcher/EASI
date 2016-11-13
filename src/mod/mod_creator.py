# coding=utf-8

from re import compile

from src.easi.ops import long_input, \
    create_new_mod_collect_basics
from src.low import constants
from src.low.custom_logging import make_logger
from src.meta_repo.local_meta_repo import LocalMetaRepo
from src.sig import SIG_CREATE_NEW_MOD, SigMsg
from src.low.custom_path import Path

logger = make_logger(__name__)
RE_MOD_NAME = compile(""".*[a-zA-Z]{4,}.*""")


class ModCreator:
    def __init__(self, meta_repo_name=None):
        self.basics = create_new_mod_collect_basics(constants.MAIN_UI, meta_repo_name)
        if self.basics:
            self.create_draft_mod_object()

    def create_draft_mod_object(self):
        meta_repo = LocalMetaRepo()[self.basics['meta_repo_name']]
        mod = meta_repo.create_new_mod(self.basics['mod_name'])
        mod.meta.category = self.basics['category']
        mod.meta.version = self.basics['mod_version']
        mod.meta.dcs_version = self.basics['dcs_version']
        mod.meta.description = self.basics['mod_desc']
        mod.meta.status = 'draft'
        mod.meta.write()
        Path(mod.local_folder.joinpath('DCS')).makedirs_p()
        Path(mod.local_folder.joinpath('Saved Games')).makedirs_p()

    def _get_desc(self):
        desc = long_input(
            title='Mod description',
            text='(optional)\n\nEnter a short description of your mod:',
            parent=constants.MAIN_UI
        )
        if desc:
            self.__mod_desc = desc
        return True

    @staticmethod
    def _create_mod_object():
        # self.__mod = self.meta_repo.create_new_mod(self.__mod_name)
        # self.mod.meta.category = self.__mod_category
        # self.mod.meta.dcs_version = self.__dcs_version
        # self.mod.meta.version = self.__mod_version
        # self.mod.meta.description = self.__mod_desc
        # self.mod.meta.status = 'draft'
        # self.mod.meta.write()
        SigMsg().show('Draft saved', 'Your draft for "{}" has been saved.\n\n'
                                     'I am now going to open ')

    def _select_hosting_provider(self):
        pass
        # choices =

    def _create_fs_stub(self):
        pass


def init_mod_creator():
    logger.info('initializing')

    def on_sig_create_new_mod(sender, meta_repo_name):
        logger.debug('catched mod creation request from: {}'.format(sender))
        ModCreator(meta_repo_name=meta_repo_name)

    SIG_CREATE_NEW_MOD.connect(on_sig_create_new_mod, weak=False)

    logger.info('initializing')
