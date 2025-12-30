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
from datetime import timedelta

import pytest
from faker import Faker
from faker.providers import company, lorem, date_time

from pytito import AdminAPI


@pytest.fixture(scope='function', name='mocked_environment_api_key')
def mocked_environment_api_key_implementation(mocker):
    """
    Mock the API key in the environment variables
    """

    key = 'fake_environment_var_api_key'

    mocker.patch.dict('os.environ', {'TITO_API_KEY': key})

    yield key


# pylint:disable-next=too-few-public-methods
class Event:
    """
    Event within the data model of the mocked data
    """
    faker: Optional[Faker] = None

    def __init__(self, date_range_start, date_range_end):
        if self.faker is None:
            self.faker = Faker()
            self.faker.add_provider(lorem)
            self.faker.add_provider(date_time)

        self.title = ' '.join(self.faker.words(3))
        self.description = self.faker.paragraph(nb_sentences=3,
                                                variable_nb_sentences=True)
        self.start_at = self.faker.date_time_between_dates(
            datetime_start=date_range_start,
            datetime_end=date_range_end).astimezone()

    @property
    def slug(self) -> str:
        """
        slug used to form the end_point of the api
        """
        return self.title.replace(' ', '-')


# pylint:disable-next=too-few-public-methods
class Account:
    """
    Account with in the data model of the mocked data
    """
    faker: Optional[Faker] = None

    def __init__(self):
        if self.faker is None:
            self.faker = Faker()
            self.faker.add_provider(company)

        self.name = self.faker.bs()
        self.description = self.faker.catch_phrase()

        # future events
        self.events: list[Event] = [Event(date_range_start=timedelta(days=1),
                                          date_range_end=timedelta(days=365)) for _ in range(5)]

    @property
    def slug(self) -> str:
        """
        slug used to form the end_point of the api
        """
        return self.name.replace(' ', '-')


@pytest.fixture(scope='function', name='mocked_data')
def mocked_data_implementation():
    """
    Test fixture to generate a set of mocked data for the use in various tests
    """
    yield [Account() for _ in range(2)]


@pytest.fixture(scope='function', name='mocked_admin_api')
def mocked_admin_api_implementation(requests_mock, mocked_data):
    """
    A test fixture that provides an mocked AdminAPI with mocked data
    """

    # pylint:disable-next=unused-argument
    def hello_json_content(request, context):
        return {'accounts': [item.slug for item in mocked_data]}

    requests_mock.get("https://api.tito.io/v3/hello", status_code=200,
                      json=hello_json_content)
    for account in mocked_data:
        requests_mock.get(f"https://api.tito.io/v3/{account.slug}", status_code=200,
                          json={'account': {'name': account.name, 'slug': account.slug}})
        requests_mock.get(f"https://api.tito.io/v3/{account.slug}/events", status_code=200,
                          json={'events': [
                              {'_type':'event',
                               'title': event.title,
                               'slug': event.slug,
                               'start_at': event.start_at.isoformat(timespec='milliseconds'),
                               'account_slug': account.slug}
                              for event in account.events]})

    yield AdminAPI(api_key='fake_api_key')
