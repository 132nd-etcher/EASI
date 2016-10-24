# coding=utf-8
import os
from json import dumps
from src.dcs.dcs_installs import DCSInstalls
from src.cfg.cfg import Config
from src.low.custom_logging import make_logger
from src.low.custom_path import Path

logger = make_logger(__name__)


def parse_local_folder_into_mod_metadata():
    dcs_install_dir, _, _ = getattr(DCSInstalls(), Config().active_dcs_installation)
    d = {'known_assets': [os.path.basename(x) for x in Path(dcs_install_dir).joinpath('Bazar/Liveries').listdir()]}
    print(d)
    # with open('known_assets.json', 'w') as f:
    #     f.write(dumps(d, indent=True))


if __name__ == '__main__':
    DCSInstalls().discover_dcs_installation()
    parse_local_folder_into_mod_metadata()
