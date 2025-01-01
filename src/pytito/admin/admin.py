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

This file provides the admin api root class
"""
from typing import Optional

from ._base_client import AdminAPIBase
from .account import Account


class AdminAPI(AdminAPIBase):
    """
    Instance of the Tito IO Admin API
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, api_key:Optional[str]=None) -> None:
        super().__init__(json_content=None, api_key=api_key)
        self._populate_json()
        self.accounts = {account_slug:Account(account_slug=account_slug, api_key=api_key)
                         for account_slug in self.__account_slugs}

    @property
    def _end_point(self) -> str:
        return super()._end_point

    def _populate_json(self) -> None:
        self._json_content = self._get_response('hello')

    @property
    def __account_slugs(self) -> list[str]:
        """
        All the account slugs associated with the admin API key
        """
        if not isinstance(self._json_content['accounts'], list):
            raise TypeError('accounts should be a list')
        return self._json_content['accounts']
