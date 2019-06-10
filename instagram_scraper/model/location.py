# -*- coding:utf-8 -*-

from instagram_scraper.model.base_model import BaseModel


class Location(BaseModel):

    def __init__(self, props=None):
        self._init_properties_map = {
            'id': '_id',
            'has_public_page': '_has_public_page',
            'name': '_name',
            'slug': '_slug',
            'lat': '_lat',
            'lng': '_lng',
            'modified': '_modified'
        }
        self._id = ''
        self._has_public_page = False
        self._name = ''
        self._slug = ''
        self._lat = ''
        self._lng = ''
        self._modified = ''
        super(Location, self).__init__(props)

    def get_id(self):
        return self._id

    def get_has_public_page(self):
        return self._has_public_page

    def get_name(self):
        return self._name

    def get_slug(self):
        return self._slug

    def get_lng(self):
        return self._lng

    def get_lat(self):
        return self._lat

    def get_modified(self):
        return self._modified
