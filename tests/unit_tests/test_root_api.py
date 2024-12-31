"""
pytito is a python wrapper for the tito.io API
Copyright (C) 2024

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This module is for testing root of the admin api
"""
import pytest

from pytito import AdminAPI
from pytito.admin import UnauthorizedException


def test_local_api_key_connection(requests_mock):
    """
    Check that if there is an API key provided it does not use the one from the environment
    variables
    """
    requests_mock.get("https://api.tito.io/v3/hello", status_code=200,
                      json={'accounts':['account1_slug']})
    _ = AdminAPI('provided_key')

    assert requests_mock.called
    assert len(requests_mock.request_history) == 1
    request_headers = requests_mock.request_history[0].headers
    assert 'Authorization' in request_headers
    assert request_headers['Authorization'] == "Token token=provided_key"


def test_environment_api_key_connection(requests_mock, mocked_environment_api_key):
    """
    Check that the default behaviour is to use the environment variable
    """
    requests_mock.get("https://api.tito.io/v3/hello", status_code=200,
                      json={'accounts':['account1_slug']})
    _ = AdminAPI()

    assert requests_mock.called
    assert len(requests_mock.request_history) == 1
    request_headers = requests_mock.request_history[0].headers
    assert 'Authorization' in request_headers
    assert request_headers['Authorization'] == f"Token token={mocked_environment_api_key}"


def test_failed_connection(requests_mock, mocked_environment_api_key):
    """
    Check that the default behaviour is to use the environment variable
    """
    requests_mock.get("https://api.tito.io/v3/hello", status_code=401,
                      json={'message':'bad API key'})
    with pytest.raises(UnauthorizedException):
        _ = AdminAPI()

    assert requests_mock.called
    assert len(requests_mock.request_history) == 1
    request_headers = requests_mock.request_history[0].headers
    assert 'Authorization' in request_headers
    assert request_headers['Authorization'] == f"Token token={mocked_environment_api_key}"
