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

This file provides the base class for the AdminAPI classses
"""
import os
from abc import ABC
from typing import Any

import requests


class UnpopulatedException(Exception):
    """
    Exception for attempting to access a property of the event if the json has not been
    populated
    """


class AdminAPIBase(ABC):
    """
    Base Class for the Tito IO Admin APIs
    """
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        pass

    def __api_key(self) -> str:
        return os.environ['TITO_API_KEY']

    @property
    def _end_point(self) -> str:
        return "https://api.tito.io/v3"

    def _get_response(self, endpoint: str) -> dict[str, Any]:

        full_end_point = self._end_point + '/' + endpoint

        response = requests.get(
            full_end_point,
            headers={"Accept": "application/json",
                     "Authorization": f"Token token={self.__api_key()}"}
        )

        if not response.status_code == 200:
            raise RuntimeError('Hello failed')

        return response.json()
