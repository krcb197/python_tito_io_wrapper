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

from ._base_client import EventChildAPIBase, optional_datetime_from_json, datetime_to_json

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

    def _update(self, payload: dict[str, Any]) -> None:
        self._patch_reponse(value={'activity': payload})
        for key, value in payload.items():
            self._json_content[key] = value

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

    @start_at.setter
    def start_at(self, value: Optional[datetime]) -> None:
        payload : dict[str, Any]
        if value is None:
            if self.end_at is not None:
                raise RuntimeError('The activity is not allowed end time without a start, '
                                   'set the end_at to None first')
            payload = {'date': None,
                       'start_time': None}
            self._patch_reponse(value={'activity': payload})
            self._json_content['start_at'] = None
        else:
            if self.end_at is not None and self.end_at.date() != value.date():
                raise ValueError('The start_at and end_at must share a common date, '
                                 'you may need to set the end date to None to mke this change')
            if self.end_at is not None and value >= self.end_at:
                raise ValueError(f'new start_at ({value}) is after the end_at ({self.end_at})')
            # the start_at can not be changed directly, instead it is necessary to modify the
            # date and time
            payload = {'date': value.strftime("%Y-%m-%d"),
                       'start_time': value.strftime("%H:%M")}
            self._patch_reponse(value={'activity': payload})
            value_str = datetime_to_json(value)
            self._json_content['start_at'] = value_str

    @property
    def end_at(self) -> Optional[datetime]:
        """
        End date and time for the activity
        """
        # There is an anomaly that the end_at reports a value if the `end_time` is none but the
        # date is set to sometime
        if self._json_content['end_time'] is None:
            return None
        json_value = self._json_content['end_at']
        return optional_datetime_from_json(json_value=json_value)

    @end_at.setter
    def end_at(self, value: Optional[datetime]) -> None:
        payload: dict[str, Any]
        if value is None:
            payload = {'end_time': None}
            self._patch_reponse(value={'activity': payload})
            self._json_content['end_at'] = None
        else:
            if self.start_at is None:
                raise ValueError('An activity needs to have a start time to allow an end time'
                                 ' to be sent, please configure the start_at first')
            if self.start_at.date() != value.date():
                raise ValueError('The start_at and end_at must share a common date')
            if value <= self.start_at:
                raise ValueError(f'new end_at ({value}) is before the start_at ({self.start_at})')
            # the start_at can not be changed directly, instead it is necessary to modify the
            # date and time
            payload = {'end_time': value.strftime("%H:%M")}
            self._patch_reponse(value={'activity': payload})
            value_str = datetime_to_json(value)
            self._json_content['end_at'] = value_str
