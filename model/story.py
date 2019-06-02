# -*- coding:utf-8 -*-

from model.media import Media


class Story(Media):

    def __init__(self, props=None):
        """
        We do not need some values - do not parse it for Story,
        for example - we do not need owner object inside story
        :param props:
        """
        self.__skip_prop = {
            'owner': True
        }
        super(Story, self).__init__(props)

    def _init_properties_custom(self, value, prop, dictionary=None):
        if self.__skip_prop:
            return False
        super(Story, self)._init_properties_custom(value, prop, dictionary)
