import os
from dataclasses import dataclass
from typing import Any

import pytest


@pytest.fixture(scope='function', name='mocked_requests')
def mocked_requests_implementation(mocker):
    """
    fixture which mock the python requests module
    """
    def http_get(*args, **kwargs):
        response = mocker.MagicMock()
        response.status_code = 200
        return response

    mocker.patch('requests.get', side_effect=http_get)
    mocker.patch.dict('os.environ', {'TITO_API_KEY': 'fake_enviroment_var_api_key'})

    yield


