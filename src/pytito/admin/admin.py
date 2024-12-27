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

from ._base_client import AdminAPIBase
from .account import Account


class AdminAPI(AdminAPIBase):
    """
    Instance of the Tito IO Admin API
    """
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        account_slugs = self.hello()
        self.accounts = {account_slug:Account(account_slug=account_slug)
                         for account_slug in account_slugs}

    @property
    def _end_point(self) -> str:
        return super()._end_point

    def hello(self) -> list[str]:
        """
        Calls the hello API to confirm a connection

        return:
            list of authorised accounts
        """

        return self._get_response('hello')['accounts']
