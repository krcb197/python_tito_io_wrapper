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
import time

from datetime import datetime

from ._base_client import AdminAPIBase, datetime_from_json, datetime_to_json
from .ticket import Ticket
from .release import Release
from .activity import Activity


class Event(AdminAPIBase):
    """
    One of the events available through the Tito IO AdminAPI
    """

    def __init__(self, *, account_slug:str, event_slug:str,
                 json_content:Optional[dict[str, Any]]=None,
                 api_key: Optional[str] = None,
                 allow_automatic_json_retrieval:bool=False) -> None:
        super().__init__(json_content=json_content, api_key=api_key,
                         allow_automatic_json_retrieval=allow_automatic_json_retrieval)
        self.__account_slug = account_slug
        self.__event_slug = event_slug
        self.__api_key_internal = api_key
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

    def _populate_json(self) -> None:
        self._json_content = self._get_response(endpoint='')['event']
        if self._json_content['_type'] != "event":
            raise ValueError('JSON content type was expected to be ticket')

    def _update(self, payload: dict[str, Any]) -> None:
        self._patch_response(value={'event': payload})
        for key, value in payload.items():
            self._json_content[key] = value

    def _update_slug(self, new_slug: str) -> None:
        """
        The Slug is a unique component of the data used to reference the release in the API.
        It is sometimes desirable to change this

        .. Warning::
            Changing the slug may break things, especially if it clashes with another slug.
            Use this method with caution. In particular, the slug is used to key other
            dictionaries within the data model. Once changing the clug it is recommended that
            the whole data model is refreshed
        """
        self._update({'slug': new_slug})
        self.__event_slug = new_slug

    @property
    def title(self) -> str:
        """
        Event title
        """
        return self._json_content['title']

    @title.setter
    def title(self, value: str) -> None:
        self._update({'title': value})

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

    @start_at.setter
    def start_at(self, value: datetime) -> None:
        if value >= self.end_at:
            raise ValueError(f'new start_at ({value}) is after the end_at ({self.end_at})')
        # the start_at can not be changed directly, instead it is necessary to modify the
        # date and time
        payload = {'start_date': value.strftime("%Y-%m-%d"),
                   'start_time': value.strftime("%H:%M")}
        self._patch_response(value={'event': payload})
        value_str = datetime_to_json(value)
        self._json_content['start_at'] = value_str

    @property
    def end_at(self) -> datetime:
        """
        End date and time for the event
        """
        json_content = self._json_content['end_at']
        return datetime_from_json(json_value=json_content)

    @end_at.setter
    def end_at(self, value: datetime) -> None:
        if value <= self.start_at:
            raise ValueError(f'new end_at ({value}) is before the start_at ({self.start_at})')
        # the end_at can not be changed directly, instead it is necessary to modify the
        # date and time
        payload = {'end_date': value.strftime("%Y-%m-%d"),
                   'end_time': value.strftime("%H:%M")}
        self._patch_response(value={'event': payload})
        value_str = datetime_to_json(value)
        self._json_content['end_at'] = value_str

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

    @property
    def live(self) -> bool:
        """
        Whether the event is live (or draft)
        """
        return self._json_content['live']

    @property
    def test_mode(self) -> bool:
        """
        Whether the event is in test mode
        """
        return self._json_content['test_mode']

    def duplicate_event(self, title:str, slug:Optional[str]=None) -> "Event":
        """
        Duplicate the event and then update the title and optionally the new slug for the
        created event
        :param title: New event title
        :param slug: New event slug, a value of None will leave the automatically created slug in
                     place
        :return: The newly created event
        """
        self._post_response('duplication', value={})
        for _ in range(120):
            time.sleep(1)
            duplication_status = self._get_duplication_status()
            status = duplication_status['status']
            if status == 'processing':
                # pylint:disable-next=bad-builtin
                print('Duplication in progress')
                continue
            if status == 'complete':
                new_slug = duplication_status['slug']
                new_title = duplication_status['title']
                new_event = Event(account_slug=self.__account_slug,
                                  event_slug=new_slug,
                                  json_content=None,
                                  api_key=self.__api_key_internal,
                                  allow_automatic_json_retrieval=True)
                if new_event.title != new_title:
                    raise ValueError(f'New event has different title to reported value:{new_title}')
                new_event.title = title
                if slug is not None:
                    # The update slug method is a powerful option that is not normally exposed
                    # to the users so is private
                    # pylint:disable-next=protected-access
                    new_event._update_slug(slug)
                return new_event

            raise ValueError('Unhandled {status=}')

        raise RuntimeError('Timeout During Event Duplication')

    def _get_duplication_status(self) -> dict[str, Any]:
        duplication_status = self._get_response('duplication')['duplication']
        if duplication_status['_type'] != '_duplication':
            raise RuntimeError('Duplication response does not have a value of _type=_duplication')
        return duplication_status

    def _delete_event(self) -> None:
        """
        Delete the event
        """
        self._delete_response()
