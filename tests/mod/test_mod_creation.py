# coding=utf-8

from unittest import mock
import string

import pytest
from pytestqt.qtbot import QtBot
import semver
from hypothesis import strategies as st, given

from src.low import constants
from src.low.singleton import Singleton
from src.mod import create_new_mod
from src.mod.mod_objects import mod_draft
from src.rem.gh.gh_session import GHSession
from src.ui.dialog_edit_mod.dialog import NewModDialog
from src.ui.form_mod_metadata.form import FormModMetadata


class TestModCreation:
    def test_gh_account_is_valid(self):
        Singleton.wipe_instances('GHSession')
        create_new_mod.GHLoginDialog.make = gh_login_dialog = mock.MagicMock()
        create_new_mod.ConfirmDialog.make = confirm_dialog = mock.MagicMock()
        confirm_dialog.return_value = False
        create_new_mod.gh_account_is_valid()
        confirm_dialog.assert_called_with('Creating a mod requires a valid Github account.<br><br>'
                                          'Would you like to connect your Github account now?',
                                          'Github account not connected')
        gh_login_dialog.assert_not_called()
        confirm_dialog.return_value = True
        create_new_mod.gh_account_is_valid()
        gh_login_dialog.assert_called_with(constants.MAIN_UI)
        gh_login_dialog.reset_mock()

    def test_gh_account_is_valid_with_gh_session(self, secret):
        create_new_mod.GHLoginDialog.make = gh_login_dialog = mock.MagicMock()
        create_new_mod.ConfirmDialog.make = mock.MagicMock()
        Singleton.wipe_instances('GHSession')
        GHSession(secret.gh_test_token)
        create_new_mod.gh_account_is_valid()
        gh_login_dialog.assert_not_called()

    def test_collect_basic_meta_data(self, tmpdir):
        draft = mod_draft.ModDraft('testing')
        assert draft.path == str(tmpdir.join('own_mods').join('testing.easi_mod_draft'))
        create_new_mod.NewModDialog.make = new_mod_dialog = mock.MagicMock()
        create_new_mod.collect_basic_meta_data(draft, None)
        new_mod_dialog.assert_called_with(draft, None)

    def test_create_draft_repository(self, tmpdir, random_mod_name):
        draft = mod_draft.ModDraft('testing')
        draft.name = random_mod_name
        assert not draft.repo_path.exists()
        assert draft.path == str(tmpdir.join('own_mods').join('testing.easi_mod_draft'))
        assert create_new_mod.create_draft_repository(draft, None)
        assert draft.repo_path.exists()

    def test_add_content(self, tmpdir, random_mod_name):
        with mock.patch('src.mod.create_new_mod.MsgDialog', autospec=True) as msg, \
                mock.patch('src.mod.create_new_mod.ModFilesDialog', autospec=True) as mod_files, \
                mock.patch('os.startfile') as start_file:
            draft = mod_draft.ModDraft('testing')
            draft.name = random_mod_name
            create_new_mod.add_content(draft, None)
            msg.assert_called_with()
            assert msg.method_calls == [
                mock.call().show(
                    'Success',
                    'Your mod has been created!\n\n'
                    'I\'m going to open it for you, so you may begin adding content to it.\n\n'
                    'WARNING: there is a ".git" folder within you mod folder; do not touch it unless you know '
                    'what you\'re doing ! =)'),
                mock.call().qobj.exec()
            ]
            start_file.assert_called_with(draft.repo_path)
            mod_files.assert_called_with(draft, None)
            assert mod_files.method_calls == [
                mock.call().qobj.exec()
            ]


class TestNewModDialog:
    @pytest.fixture(params=[
        ('maj', semver.bump_major),
        ('min', semver.bump_minor),
        ('pat', semver.bump_patch),
        ('pre', semver.bump_prerelease),
        ('bui', semver.bump_build),
    ])
    def ver(self, request):
        yield request.param

    # noinspection PyShadowingNames
    @pytest.fixture()
    def form(self, qtbot, mod_draft):
        assert isinstance(mod_draft, create_new_mod.ModDraft)
        dialog = NewModDialog(mod_draft)
        qtbot.add_widget(dialog.qobj)
        f = dialog.qobj.form
        assert f.label_uuid.text() == mod_draft.uuid
        assert f.edit_mod_name.text() == ''
        assert f.edit_version.text() == '0.0.1'
        assert f.edit_dcs_version.text() == ''
        assert f.error_widget is None
        yield f
        dialog.qobj.reject()

    # noinspection PyShadowingBuiltins
    @given(maj=st.integers(min_value=0, max_value=32),
           min=st.integers(min_value=0, max_value=32),
           pat=st.integers(min_value=0, max_value=32),
           pre=st.integers(min_value=0, max_value=32),
           bui=st.integers(min_value=0, max_value=32),
           )
    def test_increment_version(self, maj, min, pat, pre, bui, form: FormModMetadata, ver):
        new_semver = '{}.{}.{}{}{}'.format(
            maj, min, pat,
            '-rc.{}'.format(pre) if pre > 0 else '',
            '+{}'.format(bui) if bui > 0 else '',
        )
        assert isinstance(semver.parse(new_semver), dict)
        form.load_data_from_meta()
        assert form.edit_version.text() == '0.0.1'
        form.edit_version.setText(new_semver)
        form.version_menu[ver[0]][0].trigger()
        assert form.edit_version.text() == ver[1](new_semver)

    @given(name=st.text(min_size=4, max_size=32, alphabet=string.ascii_letters))
    def test_set_good_name(self, name, form: FormModMetadata, qtbot: QtBot):
        with mock.patch('src.ui.form_mod_metadata.form.LocalMod.mod_name_is_available') as mod_name_is_available:
            mod_name_is_available.return_value = True
            form.load_data_from_meta()
            form.combo_category.setCurrentIndex(1)
            form.edit_mod_name.setText(name)
            form.edit_mod_name.textChanged.emit(str(name))
            qtbot.wait_until(lambda: form._meta_has_changed is True)
            qtbot.wait_until(lambda: form._meta_is_valid is True)
            assert form.error_widget is None

    @given(name=st.one_of(st.integers(), st.text(min_size=1, max_size=3)))
    def test_set_wrong_name(self, name, form: FormModMetadata, qtbot: QtBot):
        with mock.patch('src.ui.form_mod_metadata.form.LocalMod.mod_name_is_available') as mod_name_is_available:
            mod_name_is_available.return_value = True
            form.load_data_from_meta()
            form.combo_category.setCurrentIndex(1)
            form.edit_mod_name.setText(str(name))
            qtbot.wait_until(lambda: form._meta_has_changed is True)
            qtbot.wait_until(lambda: form._meta_is_valid is False)
            assert form.error_widget is None

    @given(category_index=st.integers(min_value=1, max_value=3))
    def test_set_category(self, category_index, form: FormModMetadata, qtbot: QtBot):
        with mock.patch('src.ui.form_mod_metadata.form.LocalMod.mod_name_is_available') as mod_name_is_available:
            mod_name_is_available.return_value = True
            form.load_data_from_meta()
            form.edit_mod_name.setText('aaaa')
            form.combo_category.setCurrentIndex(category_index)
            qtbot.wait_until(lambda: form._meta_has_changed is True)
            qtbot.wait_until(lambda: form._meta_is_valid is True)
            assert form.error_widget is None
