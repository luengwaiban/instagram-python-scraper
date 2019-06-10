# -*- coding:utf-8 -*-
from instagram_scraper.model.base_model import BaseModel


class Tag(BaseModel):

    def __init__(self, props=None):
        self._init_properties_map = {
            'media_count': '_media_count',
            'name': '_name',
            'id': '_id'
        }
        self._media_count = 0
        self._name = ''
        self._id = ''
        super(Tag, self).__init__(props)

    def get_media_count(self):
        return self._media_count

    def get_name(self):
        return self._name

    def ge_id(self):
        return self._id
