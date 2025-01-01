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
from typing import Any, Optional

import requests


class UnpopulatedException(Exception):
    """
    Exception for attempting to access a property of the event if the json has not been
    populated
    """


class UnauthorizedException(Exception):
    """
    Exception for the request not being authenticated
    """


class AdminAPIBase(ABC):
    """
    Base Class for the Tito IO Admin APIs
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, json_content:Optional[dict[str, Any]]=None,
                 api_key:Optional[str]=None,
                 allow_automatic_json_retrieval:bool=False) -> None:
        self.__api_key_internal = api_key
        self.__json_content = json_content
        self.__allow_automatic_json_retrieval = allow_automatic_json_retrieval

    def __api_key(self) -> str:
        if self.__api_key_internal is None:
            return os.environ['TITO_API_KEY']
        return self.__api_key_internal

    @property
    def _json_content(self) -> dict[str, Any]:
        if self.__json_content is None:
            if self.__allow_automatic_json_retrieval:
                self._populate_json()

        if self.__json_content is None:
            raise UnpopulatedException('json content is not populated')

        return self.__json_content

    @_json_content.setter
    def _json_content(self, content: dict[str, Any]) -> None:
        self.__json_content = content

    @property
    def _end_point(self) -> str:
        return "https://api.tito.io/v3"

    def _populate_json(self) -> None:
        self.__json_content = self._get_response(endpoint='')

    def _get_response(self, endpoint: str) -> dict[str, Any]:

        if endpoint == '':
            full_end_point = self._end_point
        else:
            full_end_point = self._end_point + '/' + endpoint

        response = requests.get(
            url=full_end_point,
            headers={"Accept": "application/json",
                     "Authorization": f"Token token={self.__api_key()}"},
            timeout=10.0
        )

        if response.status_code == 401:
            raise UnauthorizedException(response.json()['message'])

        if not response.status_code == 200:
            raise RuntimeError(f'Hello failed with status code: {response.status_code}')

        return response.json()
