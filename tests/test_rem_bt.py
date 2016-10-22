# coding=utf-8

import os
from json import loads, dumps

import pytest
import requests
from httmock import response, urlmatch, with_httmock

from src.low.custom_path import Path
from src.rem.bt.bt_session import BTSession
from src.rem.bt.bt_objects.bt_file import BTFile, BTAllFiles
from src.rem.bt.bt_objects.bt_version import BTVersion

ENDPOINT = r'(.*\.)?api\.bintray\.com$'
HEADERS = {'content-type': 'application/json'}
GET = 'get'
PATCH = 'patch'


class BTResource:
    def __init__(self, path):
        self.path = path

    def get(self):
        return Path(self.path).text()

    def patch(self, request):
        req_j = request.body.decode()
        req_d = loads(req_j)
        local_j = Path(self.path).text()
        local_d = loads(local_j)
        assert isinstance(local_d, dict)
        local_d.update(req_d)
        local_j = dumps(local_d)
        return response(200, local_j, HEADERS, 'OK', 5, request)


current_user = 'octocat'


def check_fail(url, request):
    if url.path.endswith('le_resp_is_empty'):
        return None
    if url.path.endswith('le_api_is_down'):
        return response(500, None, HEADERS, 'Error', 5, request)
    if url.path.endswith('le_rate_is_exceeded'):
        return response(403, {'message': 'API rate limit exceeded for '}, HEADERS, 'Error', 5, request)
    if url.path.endswith('le_random_error'):
        return response(402, {'message': 'Random message'}, HEADERS, 'Error', 5, request)
    return 'ok'


def get_file_path(url):
    if '/user/' in url.path:
        file_path = url.netloc + url.path.replace('/user/', '/user/{}/'.format(current_user)) + '.json'
    else:
        file_path = url.netloc + url.path + '.json'
    if not os.path.exists(file_path):
        file_path = 'tests/{}'.format(file_path)
    return file_path


@urlmatch(netloc=ENDPOINT)
def mock_bt_api(url, request):
    assert isinstance(request, requests.models.PreparedRequest)
    fail = check_fail(url, request)
    if not fail == 'ok':
        return fail
    file_path = get_file_path(url)
    try:
        if request.method == 'GET':
            content = BTResource(file_path).get()
        elif request.method == 'PATCH':
            content = BTResource(file_path).patch(request)
        else:
            raise ValueError('request not handled: {}'.format(request.method))
    except EnvironmentError:
        print('file not found locally, mocking 404')
        return response(404, {}, HEADERS, 'FileNotFound: {}'.format(file_path), 5, request)
    return response(200, content, HEADERS, 'Success', 5, request)


def test_init():
    assert BTSession() is BTSession()


def test_build_req():
    s = BTSession()
    assert s.build_req('test', 'test') == 'https://api.bintray.com/test/test'
    with pytest.raises(ValueError):
        s.build_req()
    with pytest.raises(TypeError):
        s.build_req(1)


# noinspection SpellCheckingInspection
@with_httmock(mock_bt_api)
def test_get_files_for_package():
    s = BTSession()
    files = s.get_files_for_package('alpha')
    assert isinstance(files, BTAllFiles)
    assert len(files) == 1
    file = files['nutcracker-1.1-sources.jar']
    assert isinstance(file, BTFile)
    assert file.version == '1.1'
    assert file.sha1 == '602e20176706d3cc7535f01ffdbe91b270ae5012'
    assert file.name == 'nutcracker-1.1-sources.jar'
    assert file.path == 'org/jfrog/powerutils/nutcracker/1.1/nutcracker-1.1-sources.jar'
    assert file.package == 'jfrog-power-utils'
    assert file.repo == 'jfrog-jars'
    assert file.owner == 'jfrog'
    assert file.created == "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)"
    assert file.size == 1234


# noinspection SpellCheckingInspection
@with_httmock(mock_bt_api)
def test_get_latest_version():
    s = BTSession()
    latest = s.get_latest_version('alpha')
    assert isinstance(latest, BTVersion)
    assert latest.name == '1.1.5'
    assert latest.desc == 'This version...'
    assert latest.repo == 'repo'
    assert latest.owner == 'user'
    assert latest.created == "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)"
    assert latest.updated == "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)"
    assert latest.released == "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)"
    assert latest.vcs_tag == ''
    assert latest.ordinal == 5
    assert latest.github_release_notes_file == ''
    assert latest.github_use_tag_release_notes == ''
