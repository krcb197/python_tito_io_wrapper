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

import pytest


@pytest.fixture(scope='function', name='mocked_environment_api_key')
def mocked_environment_api_key_implementation(mocker):
    """
    Mock the API key in the environment variables
    """

    key = 'fake_environment_var_api_key'

    mocker.patch.dict('os.environ', {'TITO_API_KEY': key})

    yield key
