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

This module is for testing root of the account
"""
from pytito.admin import Account


def test_accounts(mocked_data, mocked_admin_api):
    """
    Check the accounts are instantiated correctly
    """
    for data_model_account, (admin_api_account_slug, admin_api_account) in \
            zip(mocked_data, mocked_admin_api.accounts.items()):
        assert isinstance(admin_api_account, Account)
        assert data_model_account.slug == admin_api_account_slug


def test_account_attributes(mocked_data, mocked_admin_api):
    """
    check that the data is properly populated with in the account when requested
    """
    for data_model_account, admin_api_account in \
            zip(mocked_data, mocked_admin_api.accounts.values()):
        assert data_model_account.name == admin_api_account.name


def test_account_events(mocked_data, mocked_admin_api):
    """
    test that the list of upcoming events is served up correctly
    """
    for data_model_account, admin_api_account in \
            zip(mocked_data, mocked_admin_api.accounts.values()):
        for data_model_event, (event_slug, event) in \
            zip(data_model_account.events, admin_api_account.events.items()):
            assert data_model_event.title == event.title
            assert data_model_event.slug == event_slug


def test_account_next_event(mocked_data, mocked_admin_api):
    """
    Test that the next event is report correctly
    """
    for data_model_account, admin_api_account in \
            zip(mocked_data, mocked_admin_api.accounts.values()):
        data_model_next_event = sorted(data_model_account.events, key=lambda item: item.start_at)[0]
        assert admin_api_account.next_event.title == data_model_next_event.title
