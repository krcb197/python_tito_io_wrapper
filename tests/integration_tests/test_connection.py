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

This module is for testing the connection
"""
import pytest

from pytito import AdminAPI
from pytito.admin import UnauthorizedException
from pytito.admin import Account


def test_bad_api_key():
    """
    test that using a known bad API key results in some failures
    """
    with pytest.raises(UnauthorizedException):
        _ = AdminAPI(api_key='bad_key')


def test_pytito_connection(pytito_account):
    """
    test the connection to the pytito account (used by many of the other tests) works
    correctly
    """
    assert isinstance(pytito_account, Account)
    assert pytito_account.name == 'pytito'
