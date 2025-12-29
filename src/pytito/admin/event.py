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

from datetime import datetime

from ._base_client import AdminAPIBase, datetime_from_json
from .ticket import Ticket
from .release import Release
from .activity import Activity


class Event(AdminAPIBase):
    """
    One of the events available through the Tito IO AdminAPI
    """

    def __init__(self, account_slug:str, event_slug:str,
                 json_content:Optional[dict[str, Any]]=None,
                 api_key: Optional[str] = None) -> None:
        super().__init__(json_content=json_content, api_key=api_key)
        self.__account_slug = account_slug
        self.__event_slug = event_slug
        if json_content is not None:
            if self._json_content['_type'] != "event":
                raise ValueError('JSON content type was expected to be ticket')

    @property
    def _account_slug(self) -> str:
        return self.__account_slug

    @property
    def _event_slug(self) -> str:
        return self.__event_slug

    @property
    def _end_point(self) -> str:
        return super()._end_point + f'/{self._account_slug}/{self._event_slug}'

    @property
    def title(self) -> str:
        """
        Event title
        """
        return self._json_content['title']

    def __ticket_getter(self) -> list[Ticket]:

        def ticket_factory(json_content:dict[str, Any]) -> Ticket:
            ticket_slug = json_content['slug']
            return Ticket(event_slug=self.__event_slug, account_slug=self._account_slug,
                          ticket_slug=ticket_slug, json_content=json_content)

        response = self._get_response('tickets')
        return [ticket_factory(ticket) for ticket in response['tickets']]

    @property
    def tickets(self) -> list[Ticket]:
        """
        retrieve all the tickets for the event
        """
        return self.__ticket_getter()

    @property
    def start_at(self) -> datetime:
        """
        Start date and time for the event
        """
        json_content = self._json_content['start_at']
        return datetime_from_json(json_value=json_content)

    @property
    def end_at(self) -> datetime:
        """
        End date and time for the event
        """
        json_content = self._json_content['end_at']
        return datetime_from_json(json_value=json_content)

    def __release_getter(self) -> dict[str, Release]:

        def release_factory(json_content:dict[str, Any]) -> tuple[str, Release]:
            release_slug = json_content['slug']
            return release_slug, Release(event_slug=self.__event_slug,
                                         account_slug=self._account_slug,
                                         release_slug=release_slug,
                                         json_content=json_content)

        response = self._get_response('releases')
        return dict(release_factory(release) for release in response['releases'])

    @property
    def releases(self) -> dict[str, Release]:
        """
        retrieve all the releases for the event
        """
        return self.__release_getter()

    def __activity_getter(self) -> list[Activity]:

        def activity_factory(json_content:dict[str, Any]) -> Activity:
            activity_id = json_content['id']
            return Activity(event_slug=self.__event_slug, account_slug=self._account_slug,
                            activity_id=activity_id, json_content=json_content)

        response = self._get_response('activities')
        return [activity_factory(activity) for activity in response['activities']]

    @property
    def activities(self) -> list[Activity]:
        """
        retrieve all the activities for the event
        """
        return self.__activity_getter()
