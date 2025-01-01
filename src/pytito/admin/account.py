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

This file provides the account class
"""
from typing import Optional, Any
from operator import attrgetter

from ._base_client import AdminAPIBase

from .event import Event


class Account(AdminAPIBase):
    """
    One of the accounts available through the Tito IO AdminAPI
    """

    def __init__(self, account_slug: str, json_content: Optional[dict[str, Any]] = None,
                 api_key: Optional[str] = None):
        super().__init__(json_content=json_content,
                         allow_automatic_json_retrieval=True,
                         api_key=api_key)
        self.__account_slug = account_slug
        self.__api_key_internal = api_key

    @property
    def _account_slug(self) -> str:
        return self.__account_slug

    @property
    def _end_point(self) -> str:
        return super()._end_point + f'/{self._account_slug}'

    def _populate_json(self) -> None:
        self._json_content = self._get_response(endpoint='')['account']
        if self._account_slug != self._json_content['slug']:
            raise ValueError('slug in json content does not match expected value')

    def __event_getter(self, end_point: str) -> dict[str, Event]:
        response = self._get_response(end_point)
        return_dict:dict[str, Event] = {}
        for event in response['events']:
            if event['account_slug'] != self._account_slug:
                raise RuntimeError('Account Slug inconsistency')
            slug = event['slug']
            return_dict[slug] = Event(event_slug=slug, account_slug=self._account_slug,
                                      api_key=self.__api_key_internal,
                                      json_content=event)
        return return_dict

    @property
    def events(self) -> dict[str, Event]:
        """
        Return the upcoming events
        """
        return self.__event_getter('events')

    @property
    def next_event(self) -> Event:
        """
        Return the chronologically first of the upcoming events
        """
        upcoming_events = list(self.events.values())
        upcoming_events.sort(key=attrgetter('start_at'))
        return upcoming_events[0]

    @property
    def past_events(self) -> dict[str, Event]:
        """
        Return the upcoming events
        """
        return self.__event_getter('events/past')

    @property
    def archived_events(self) -> dict[str, Event]:
        """
        Return the upcoming events
        """
        return self.__event_getter('events/archived')

    @property
    def name(self) -> str:
        """
        Account Name
        """
        return self._json_content['name']

    @property
    def description(self) -> str:
        """
        Account Description
        """
        return self._json_content['description']
