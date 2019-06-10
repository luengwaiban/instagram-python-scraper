# -*- coding:utf-8 -*-
from instagram_scraper.model.base_model import BaseModel
from instagram_scraper import model


class Comment(BaseModel):

    def __init__(self, prop=None):
        self._id = ''
        self._text = ''
        self._created_at = 0
        # Account object
        self._owner = None
        self._is_loaded = False
        super(Comment, self).__init__(prop)

    def get_id(self):
        return self._id

    def get_text(self):
        return self._text

    def get_created_at(self):
        return self._created_at

    def get_owner(self):
        return self._owner

    def _init_properties_custom(self, value, prop, dictionary=None):
        if prop == 'id':
            self._id = value
        elif prop == 'created_at':
            self._created_at = value
        elif prop == 'text':
            self._text = value
        elif prop == 'owner':
            self._owner = model.Account.create(value)
