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

This file provides the ticket class
"""
from typing import Optional, Any
import sys

from ._base_client import AdminAPIBase

if sys.version_info < (3,11):
    from strenum import StrEnum
else:
    from enum import StrEnum


class TicketState(StrEnum):
    """
    States for a ticket
    """
    NEW = 'new'
    COMPLETE = 'complete'
    INCOMPLETE = 'incomplete'
    REMINDER = 'reminder'
    VOID = 'void'


class Ticket(AdminAPIBase):
    """
    One of the tickets for an event available through the Tito IO AdminAPI
    """

    def __init__(self, account_slug:str, event_slug:str, ticket_slug:str,
                 json_content:Optional[dict[str, Any]]=None) -> None:
        super().__init__(json_content=json_content)
        self.__account_slug = account_slug
        self.__event_slug = event_slug
        self.__ticket_slug = ticket_slug

    @property
    def _account_slug(self) -> str:
        return self.__account_slug

    @property
    def _event_slug(self) -> str:
        return self.__event_slug

    @property
    def _ticket_slug(self) -> str:
        return self.__ticket_slug

    @property
    def _end_point(self) -> str:
        return super()._end_point +\
               f'/{self._account_slug}/{self._event_slug}/tickets/{self._ticket_slug}'

    def _populate_json(self) -> None:
        self._json_content = self._get_response(endpoint='')['ticket']
        if self._ticket_slug != self._json_content['slug']:
            raise ValueError('slug in json content does not match expected value')
        if self._json_content['view'] != 'extended':
            raise ValueError('expected the extended view of the ticket')

    @property
    def state(self) -> TicketState:
        """
        Event title
        """
        return TicketState(self._json_content['state'])

    @property
    def name(self) -> str:
        """
        Name of the ticket holder (First Name + Last Name)
        """
        return self._json_content['name']

    @property
    def reference(self) -> str:
        """
        Ticket reference (this is shown in guest emails) and therefore with is what ticket holder
        will consider to be their: "Ticket Number"
        """
        return self._json_content['reference']

    @property
    def answers(self) -> str:
        """
        Answers to ticket specific questions
        """
        # The answers are part of the extended data for a ticket, therefore if it is not present
        # try getting the extended view
        if 'answers' not in self._json_content:
            self._populate_json()
        return self._json_content['answers']
