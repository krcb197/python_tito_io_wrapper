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
from typing import Optional

import pytest
from faker import Faker
from faker.providers import company

from pytito import AdminAPI


@pytest.fixture(scope='function', name='mocked_environment_api_key')
def mocked_environment_api_key_implementation(mocker):
    """
    Mock the API key in the environment variables
    """

    key = 'fake_environment_var_api_key'

    mocker.patch.dict('os.environ', {'TITO_API_KEY': key})

    yield key


class Account:
    FAKER:Optional[Faker] = None

    def __init__(self):
        if self.FAKER is None:
            self.FAKER = Faker()
            self.FAKER.add_provider(company)

        self.name = self.FAKER.bs()
        self.description = self.FAKER.catch_phrase()

    @property
    def slug(self) -> str:
        return self.name.replace(' ', '-')


@pytest.fixture(scope='function', name='mocked_data')
def mocked_data_implementation(requests_mock):
    yield [Account() for _ in range(2)]


@pytest.fixture(scope='function', name='mocked_admin_api')
def mocked_admin_api_implementation(requests_mock, mocked_data):
    """
    A test fixture that provides an mocked AdminAPI with mocked data
    """
    def hello_json_content(request, context):
        return {'accounts':[item.slug for item in mocked_data] }

    requests_mock.get("https://api.tito.io/v3/hello", status_code=200,
                      json=hello_json_content)

    yield AdminAPI(api_key='fake_api_key')


