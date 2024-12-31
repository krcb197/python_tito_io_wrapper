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
import requests

import pytest

from pytito import AdminAPI

from .conftest import MockedConfig, MockedGetResponse


def test_local_api_key_connection(mocked_requests): # pylint:disable=unused-argument
    """
    Check that if there is an API key provided it does not use the one from the environment
    variables
    """
    _ = AdminAPI(api_key='fake_api_key')
    #pylint: disable-next=no-member
    requests.get.assert_called_once_with(url="https://api.tito.io/v3/hello",
                                         timeout=10.0,
                                         headers={"Accept": "application/json",
                                                  "Authorization": "Token token=fake_api_key"})


def test_environment_api_key_connection(mocked_requests):
    """
    Check that the default behaviour is to use the environment variable
    """
    _ = AdminAPI()
    # pylint: disable-next=no-member
    requests.get.assert_called_once_with(
        url="https://api.tito.io/v3/hello",
        timeout=10.0,
        headers={"Accept": "application/json",
                 "Authorization": f"Token token={mocked_requests.environment_api_key}"})


@pytest.mark.parametrize("mocked_requests",
                         [MockedConfig(mocked_get_responses={
                             'hello':MockedGetResponse(status_code=401),
                         })],
                         indirect=True)
def test_failed_connection(mocked_requests):
    """
    Check that the default behaviour is to use the environment variable
    """
    with pytest.raises(RuntimeError):
        _ = AdminAPI()

