# coding=utf-8

import shortuuid
from src.new_mod.mod import Mod
from src.repo.irepo import IRepo


class ModFactory:

    @staticmethod
    def create_new_mod(parent_meta_repo: IRepo, mod_name: str) -> Mod:
        new_mod = Mod(parent_meta_repo.local_git_repo_path.joinpath('{}.yml'.format(mod_name)), parent_meta_repo)
        new_mod.meta.uuid = shortuuid.uuid()
        new_mod.meta.name = mod_name
        return new_mod
