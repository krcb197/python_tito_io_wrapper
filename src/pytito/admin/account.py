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

from ._base_client import AdminAPIBase

from .event import Event

class Account(AdminAPIBase):
    """
    One of the accounts available through the Tito IO AdminAPI
    """

    def __init__(self, account_slug:str):
        super().__init__()
        self.__account_slug = account_slug

    @property
    def _end_point(self) -> str:
        return super()._end_point + f'/{self.__account_slug}'

    def __event_getter(self, end_point: str) -> dict[str, Event]:
        response = self._get_response(end_point)
        return_dict:dict[str, Event] = {}
        for event in response['events']:
            if event['account_slug'] != self.__account_slug:
                raise RuntimeError('Account Slug inconsistency')
            slug = event['slug']
            return_dict[slug] = Event(event_slug=slug, account_slug=self.__account_slug,
                                      json_content=event)
        return return_dict

    @property
    def events(self) -> dict[str, Event]:
        """
        Return the upcoming events
        """
        return self.__event_getter('events')

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
