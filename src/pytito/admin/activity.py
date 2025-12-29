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

This file provides the activity class
"""
from typing import Optional, Any
from datetime import datetime

from ._base_client import EventChildAPIBase, optional_datetime_from_json

class Activity(EventChildAPIBase):
    """
    One of the activities for an event available through the Tito IO AdminAPI
    """

    def __init__(self, *, account_slug:str, event_slug:str, activity_id:str,
                 json_content:Optional[dict[str, Any]]=None,
                 allow_automatic_json_retrieval: bool=False) -> None:
        super().__init__(json_content=json_content,
                         account_slug=account_slug,
                         event_slug=event_slug,
                         allow_automatic_json_retrieval=allow_automatic_json_retrieval)
        self.__activity_id = activity_id
        if json_content is not None:
            if self._json_content['_type'] != "activity":
                raise ValueError('JSON content type was expected to be activity')

    @property
    def _activity_id(self) -> str:
        return self.__activity_id

    @property
    def _end_point(self) -> str:
        return super()._end_point +\
               f'/{self._account_slug}/{self._event_slug}/activities/{self._activity_id}'

    def _populate_json(self) -> None:
        self._json_content = self._get_response(endpoint='')['id']
        if self._activity_id != self._json_content['id']:
            raise ValueError('slug in json content does not match expected value')
        if self._json_content['view'] != 'extended':
            raise ValueError('expected the extended view of the ticket')

    @property
    def name(self) -> str:
        """
        Name of the Activity
        """
        return self._json_content['name']

    @property
    def capacity(self) -> Optional[int]:
        """
        The number of people who can attend. A value of `None` means there is no limit
        """
        return self._json_content['capacity']

    @property
    def start_at(self) -> Optional[datetime]:
        """
        Start date and time for the activity
        """
        json_value = self._json_content['start_at']
        return optional_datetime_from_json(json_value=json_value)

    @property
    def end_at(self) -> Optional[datetime]:
        """
        End date and time for the activity
        """
        json_value = self._json_content['end_at']
        return optional_datetime_from_json(json_value=json_value)
