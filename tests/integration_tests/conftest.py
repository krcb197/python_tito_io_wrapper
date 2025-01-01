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

This module provides supporting test fixtures for the integration tests
"""
import pytest
from pytito import AdminAPI


@pytest.fixture(scope='session', name='admin_api')
def admin_api_implementation():
    """
    A fixture that make a connection to the real Tito server with the API key in the environment
    variables
    """
    yield AdminAPI()


@pytest.fixture(scope='function', name='pytito_account')
def pytito_account_implementation(admin_api):
    """
    A test fixture that provides an mocked AdminAPI with mocked data
    """
    yield admin_api.accounts['pytito']
