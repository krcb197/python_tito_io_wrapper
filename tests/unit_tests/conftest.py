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

This module provides supporting test fixtures for the unit test
"""
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import pytest

@dataclass()
class MockedGetResponse:
    status_code:int = 200
    json_content: dict[str, Any] = field(default_factory=dict)

    def json(self) -> dict[str, Any]:
        return self.json_content


def default_response_set() -> dict[str, MockedGetResponse]:
    """
    Default set of HTTP get responses that can be build upon for other tests
    """
    return {'hello': MockedGetResponse(status_code=200,
                                       json_content={'accounts':'account1_slug'})
            }


@dataclass()
class MockedConfig:
    """
    Configuration of this fixture
    """
    environment_api_key: str = 'fake_environment_var_api_key'
    mocked_get_responses: dict[str, MockedGetResponse] = \
        field(default_factory=default_response_set)


@pytest.fixture(scope='function', name='mocked_requests')
def mocked_requests_implementation(mocker, request):
    """
    fixture which mock the python requests module
    """
    if not hasattr(request, 'param'):
        mocking_configuration = MockedConfig()
    else:
        mocking_configuration = request.param

    def http_get(*args, **kwargs):  # pylint:disable=unused-argument
        url = kwargs.get('url')
        decomposed_url = urlparse(url)
        if decomposed_url.path.startswith('/v3/'):
            simplified_path = decomposed_url.path[4:]
            if simplified_path in mocking_configuration.mocked_get_responses:
                return mocking_configuration.mocked_get_responses[simplified_path]
            else:
                response = mocker.MagicMock()
                response.status_code = 200
                return response


    mocker.patch('requests.get', side_effect=http_get)
    mocker.patch.dict('os.environ', {'TITO_API_KEY': mocking_configuration.environment_api_key})

    yield mocking_configuration
