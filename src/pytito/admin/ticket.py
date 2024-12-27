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
from enum import StrEnum
import functools


from ._base_client import AdminAPIBase, UnpopulatedException


class UnpopulatedTicketException(UnpopulatedException):
    """
    Exception for attempting to access a property of the event if the json has not been
    populated
    """


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
        super().__init__()
        self.__account_slug = account_slug
        self.__event_slug = event_slug
        self.__ticket_slug = ticket_slug
        self.__json_content = json_content

    def __json_content_present(func):
        """Print the runtime of the decorated function"""

        @functools.wraps(func)
        def wrapper_json_content_present(self, *args, **kwargs):
            if self.__json_content is None:
                raise UnpopulatedTicketException('JSON content is not populated')
            return func(*args, **kwargs)

        return wrapper_json_content_present

    @property
    @__json_content_present
    def state(self) -> TicketState:
        """
        Event title
        """
        return TicketState(self.__json_content['state'])

    @property
    @__json_content_present
    def name(self) -> str:
        """
        Name of the ticket holder (First Name + Last Name)
        """
        return TicketState(self.__json_content['name'])
