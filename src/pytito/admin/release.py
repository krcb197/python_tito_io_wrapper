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

This file provides the release class
"""
from typing import Optional, Any
from datetime import datetime

from ._base_client import EventChildAPIBase, optional_datetime_from_json, datetime_to_json

class Release(EventChildAPIBase):
    """
    One of the release for an event available through the Tito IO AdminAPI
    """

    def __init__(self, *, account_slug:str, event_slug:str, release_slug:str,
                 json_content:Optional[dict[str, Any]]=None,
                 allow_automatic_json_retrieval: bool=False) -> None:
        super().__init__(json_content=json_content,
                         account_slug=account_slug,
                         event_slug=event_slug,
                         allow_automatic_json_retrieval=allow_automatic_json_retrieval)
        self.__release_slug = release_slug
        if json_content is not None:
            if self._json_content['_type'] != "release":
                raise ValueError('JSON content type was expected to be release')

    @property
    def _release_slug(self) -> str:
        return self.__release_slug

    @property
    def _end_point(self) -> str:
        return super()._end_point +\
               f'/{self._account_slug}/{self._event_slug}/releases/{self._release_slug}'

    def _populate_json(self) -> None:
        self._json_content = self._get_response(endpoint='')['release']
        if self._release_slug != self._json_content['slug']:
            raise ValueError('slug in json content does not match expected value')
        if self._json_content['view'] != 'extended':
            raise ValueError('expected the extended view of the ticket')
        if self._json_content['_type'] != "release":
            raise ValueError('JSON content type was expected to be release')

    def _update(self, payload: dict[str, Any]) -> None:
        self._patch_reponse(value={'release': payload})
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
        self.__release_slug = new_slug


    @property
    def title(self) -> str:
        """
        Title of the release
        """
        return self._json_content['title']

    @title.setter
    def title(self, value: str) -> None:
        self._update({'title': value})

    @property
    def secret(self) -> bool:
        """
        Title of the release
        """
        return self._json_content['secret']

    @property
    def start_at(self) -> Optional[datetime]:
        """
        Start date and time for the release being available (i.e. when is it on sale)
        """
        json_value = self._json_content['start_at']
        return optional_datetime_from_json(json_value=json_value)

    @start_at.setter
    def start_at(self, value: Optional[datetime]) -> None:
        if value is None:
            self._update({'start_at': None})
        else:
            if self.end_at is not None and value >= self.end_at:
                raise ValueError(f'new start_at ({value}) is after the end_at ({self.end_at})')
            value_str = datetime_to_json(value)
            self._update({'start_at': value_str})

    @property
    def end_at(self) -> Optional[datetime]:
        """
        End date and time for the release being available (i.e. when is it on sale)
        """
        json_value = self._json_content['end_at']
        return optional_datetime_from_json(json_value=json_value)

    @end_at.setter
    def end_at(self, value: Optional[datetime]) -> None:
        if value is None:
            self._update({'end_at': None})
        else:
            if self.start_at is not None and value <= self.start_at:
                raise ValueError(f'new end_at ({value}) is before the start_at ({self.start_at})')
            value_str = datetime_to_json(value)
            self._update({'end_at': value_str})

    @property
    def quantity(self) -> Optional[int]:
        """
        The number of tickets who can attend. A value of `None` means there is no limit
        """
        return self._json_content['quantity']
