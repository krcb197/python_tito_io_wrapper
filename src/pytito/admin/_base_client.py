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
from datetime import datetime

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

class EventChildAPIBase(AdminAPIBase, ABC):
    """
    Base Class for the children of an event e.g. Tickets, Releases, Actvities
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, *, account_slug:str, event_slug:str,
                 json_content:Optional[dict[str, Any]]=None,
                 allow_automatic_json_retrieval: bool=False) -> None:
        if json_content is None and allow_automatic_json_retrieval is False:
            raise RuntimeError('If the JSON content is not provided at initialisation, '
                               'runtime retrival is needed')
        super().__init__(json_content=json_content,
                         allow_automatic_json_retrieval=allow_automatic_json_retrieval)
        self.__account_slug = account_slug
        self.__event_slug = event_slug

    @property
    def _account_slug(self) -> str:
        return self.__account_slug

    @property
    def _event_slug(self) -> str:
        return self.__event_slug

def datetime_from_json(json_value: str) -> datetime:
    """
    convert the isoformat datetime from the json content to a python object
    """
    return datetime.fromisoformat(json_value)

def optional_datetime_from_json(json_value: str) -> Optional[datetime]:
    """
    convert the isoformat datetime from the json content to a python object, with support for
    a null (unpopulated value)
    """
    if json_value is None:
        return None
    return datetime.fromisoformat(json_value)
