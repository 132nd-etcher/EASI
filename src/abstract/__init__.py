# coding=utf-8

"""
Abstract module.

Contains everything and anything that resembles an interface.

WARNING: .ui.connected_object.py has an ugly hack in the form of a module-level member "main_ui", set at startup by
the MainUi itself, to enable Signal connectivity without breaking the abstraction.
"""

from .abstract_meta import AbstractMeta
from .abstract_progress import ProgressInterface
from .abstract_sentry import SentryContextInterface
from .mod import *
from .ui import *
