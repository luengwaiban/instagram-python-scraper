# -*- coding:utf-8 -*-
from instagram_scraper.model.initializer_model import InitializerModel


class BaseModel(InitializerModel):

    def __init__(self, props=None):
        if not hasattr(self, '_init_properties_map') or not self._init_properties_map:
            self._init_properties_map = {}
        super(BaseModel, self).__init__(props)


    def get_columns(self):
        return self._init_properties_map.keys()
