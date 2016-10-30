# coding=utf-8

import io
import webbrowser

from dropbox import Dropbox as BaseDropbox, DropboxOAuth2FlowNoRedirect, files, sharing
from dropbox.exceptions import AuthError, BadInputError, ApiError

try:
    from vault.secret import Secret
except ImportError:
    from vault.empty_secret import Secret
from src.low import constants
from src.__version__ import __version__
from src.low.singleton import Singleton
from src.low.custom_logging import make_logger
from src.low.custom_path import Path
from blinker_herald import emit, SENDER_CLASS_NAME
from src.abstract.progress_interface import ProgressInterface

logger = make_logger(__name__)


class DropboxError(Exception):
    """"""


class UploadError(DropboxError):
    """"""


class DBSession(metaclass=Singleton):
    session_status = dict(
        not_connected=0,
        connected=1,
        wrong_token=-1,
    )

    def __init__(self, token=None):
        self.agent = '{}/{}'.format(constants.APP_SHORT_NAME, __version__)
        self.session = None
        self.status = None
        self.authenticate(token)

    @emit(only='post', sender=SENDER_CLASS_NAME)
    def authenticate(self, token):
        if token is None:
            self.status = None
            return None
        try:
            self.session = BaseDropbox(token)
            account = self.session.users_get_current_account()
        except BadInputError:
            logger.error('malformed token')
            self.status = False
        except AuthError:
            logger.error('wrong token')
            self.status = False
        else:
            self.status = account.name.given_name
        finally:
            return self.status

    @property
    def vs(self) -> BaseDropbox:
        if not isinstance(self.session, BaseDropbox):
            raise DropboxError('Dropbox session not activated')
        return self.session

    @staticmethod
    def start_auth_flow():
        flow = DropboxOAuth2FlowNoRedirect(Secret.db_app_key, Secret.db_app_secret)
        webbrowser.open(flow.start(), autoraise=True)
        return flow

    @staticmethod
    def finish_auth_flow(flow, code):
        token, _ = flow.finish(code)
        return token

    def remote_path_exists(self, remote_path):
        try:
            self.vs.files_get_metadata(remote_path)
            return True
        except ApiError:
            return False

    @staticmethod
    def _validate_remote_path(remote_path: str) -> bool:
        return remote_path.startswith('/')

    def _get_sharing_link(self, remote_path) -> str:
        try:
            meta = self.vs.sharing_list_shared_links(remote_path, direct_only=True)
            links = meta.links
            while meta.has_more:
                meta = self.vs.sharing_list_shared_links(remote_path, direct_only=True, cursor=meta.cursor)
                links.extend(meta.links)
            for link in links:
                assert isinstance(link, sharing.SharedLinkMetadata)
                perm = link.link_permissions
                assert isinstance(perm, sharing.LinkPermissions)
                if perm.requested_visibility.is_public():
                    return link.url.replace('?dl=0', '?dl=1')
        except ApiError:
            raise DropboxError('error while getting links for: {}'.format(remote_path))

    def _create_sharing_link(self, remote_path) -> str:
        try:
            return self.vs.sharing_create_shared_link_with_settings(remote_path).url.replace('?dl=0', '?dl=1')
        except ApiError as e:
            if e.error.is_shared_link_already_exists():
                return self._get_sharing_link(remote_path)
            print(type(e.error), e.error)
            raise DropboxError('failed to create sharing link for {}'.format(remote_path))

    def _start_upload_session(self, first_chunk, close=False) -> files.UploadSessionStartResult:
        return self.vs.files_upload_session_start(first_chunk, close=close)

    def _finish_upload_session(self,
                               remote_path: str,
                               data: bytes,
                               cursor: files.UploadSessionCursor,
                               commit: files.CommitInfo
                               ) -> files.FileMetadata:
        try:
            return self.vs.files_upload_session_finish(data, cursor, commit)
        except ApiError:
            raise UploadError('error finishing upload of {}'.format(remote_path))

    def _upload_session_append(self,
                               remote_path: str,
                               data: bytes,
                               cursor: files.UploadSessionCursor,
                               close: bool = False) -> None:
        try:
            return self.vs.files_upload_session_append_v2(data, cursor, close)
        except ApiError:
            raise UploadError('error during upload of {}'.format(remote_path))

    def upload_data(self,
                    remote_path: str,
                    local_path: str or Path,
                    *,
                    overwrite: bool = False,
                    progress_callback: callable = None,
                    chunk_size: int = 1024 * 512):

        if not self._validate_remote_path(remote_path):
            raise UploadError('invalid remote path: {}'.format(remote_path))

        local_path = Path(local_path)
        local_data = io.BytesIO(local_path.bytes())

        mode = files.WriteMode.overwrite if overwrite else files.WriteMode.add

        link = None

        if self.remote_path_exists(remote_path):
            if not overwrite:
                raise UploadError('remote path already exists: {}'.format(remote_path))
            try:
                link = self._get_sharing_link(remote_path)
            except ApiError:
                pass

        local_size = len(local_data.getbuffer())
        local_data.seek(0)
        logger.debug('local data size: {}B'.format(local_size))

        def update_progress(value: int):
            if progress_callback:
                progress_callback((value / local_size) * 100)

        if local_size <= chunk_size:
            upload_session = self._start_upload_session(local_data)
            cursor = files.UploadSessionCursor(upload_session.session_id, local_size)
        else:
            upload_session = self._start_upload_session(local_data.read(chunk_size))
            cursor = files.UploadSessionCursor(upload_session.session_id, chunk_size)
            update_progress(cursor.offset)
        commit = files.CommitInfo(
            path=remote_path,
            mode=mode,
            autorename=False,
            mute=True
        )
        while local_data.tell() < local_size - chunk_size:
            self._upload_session_append(
                remote_path=remote_path,
                data=local_data.read(chunk_size),
                cursor=cursor,
                close=False
            )
            cursor.offset = local_data.tell()
            update_progress(cursor.offset)
        self._finish_upload_session(
            remote_path=remote_path,
            data=local_data.read(),
            cursor=cursor,
            commit=commit
        )
        cursor.offset = local_data.tell()
        update_progress(cursor.offset)

        if link is None:
            link = self._create_sharing_link(remote_path)

        return link