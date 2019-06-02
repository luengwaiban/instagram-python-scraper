# -*- coding:utf-8 -*-
from model.base_model import BaseModel


class UserStories(BaseModel):

    def __init__(self, props=None):
        self._owner = None
        self._stories = []
        super(UserStories, self).__init__(props)

    def set_owner(self, owner):
        self._owner = owner

    def get_owner(self):
        return self._owner

    def add_story(self, story):
        self._stories.append(story)

    def set_stories(self, stories):
        self._stories = stories

    def get_stories(self):
        return self._stories
