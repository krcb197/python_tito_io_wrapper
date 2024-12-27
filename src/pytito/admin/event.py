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

This file provides the event class
"""
from typing import Optional, Any

from ._base_client import AdminAPIBase, UnpopulatedException
from .ticket import Ticket

class UnpopulatedEventException(UnpopulatedException):
    """
    Exception for attempting to access a property of the event if the json has not been
    populated
    """


class Event(AdminAPIBase):
    """
    One of the events available through the Tito IO AdminAPI
    """

    def __init__(self, account_slug:str, event_slug:str,
                 json_content:Optional[dict[str, Any]]=None) -> None:
        super().__init__()
        self.__account_slug = account_slug
        self.__event_slug = event_slug
        self.__json_content = json_content

    @property
    def _end_point(self) -> str:
        return super()._end_point + f'/{self.__account_slug}/{self.__event_slug}'

    @property
    def title(self) -> str:
        """
        Event title
        """
        if self.__json_content is None:
            raise UnpopulatedEventException('title is not available')

        return self.__json_content['title']

    def __ticket_getter(self) -> list[Ticket]:

        def ticket_factory(json_content:dict[str, Any]) -> Ticket:
            ticket_slug = json_content['slug']
            return Ticket(event_slug=self.__event_slug, account_slug=self.__account_slug,
                          ticket_slug=ticket_slug, json_content=json_content)

        response = self._get_response('tickets')
        return [ticket_factory(ticket) for ticket in response['tickets']]

    @property
    def tickets(self) -> list[Ticket]:
        """
        retrieve all the tickets for the event
        """
        return self.__ticket_getter()
