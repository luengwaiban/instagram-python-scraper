# -*- coding:utf-8 -*-

from instagram_scraper.model.base_model import BaseModel


class Like(BaseModel):

    def __init__(self, props=None):
        self._id = ''
        self._username = ''
        super(Like, self).__init__(props)

    def get_id(self):
        return self._id

    def get_username(self):
        return self._username

    def _init_properties_custom(self, value, prop, dictionary=None):
        if prop == 'id':
            self._id = value
        elif prop == 'username':
            self._username = value
