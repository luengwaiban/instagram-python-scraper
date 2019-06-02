# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
import cache
import exception


class Cache(object):

    __metaclass__ = ABCMeta

    driver = 'Disk'

    @classmethod
    def create(cls, driver='Disk'):
        cls.driver = driver.capitalize()
        driver_name = cls.driver+'Cache'
        if not getattr(cache, driver_name, None):
            raise exception.InstagramError('Cache driver not found')
        return getattr(cache, driver_name, None)()

    @abstractmethod
    def get(self, key, default=None):
        """
        get the value by key
        :param key:
        :param default:
        :return:
        """
        pass

    @abstractmethod
    def set(self, key, value, ttl=0):
        """
        set a value with key, live time is optional, 0 means cache it permanently
        :param key:
        :param value:
        :param ttl:
        :return:
        """
        pass

    @abstractmethod
    def delete(self, key):
        """
        delete the value by key
        :param key:
        :return:
        """
        pass

    @abstractmethod
    def keys(self, regex=''):
        """
        get all the keys matched the Regular Expression in cache， '' means not to match
        :param regex:
        :return:
        """
        pass

    @abstractmethod
    def ttl(self, key, ttl=0):
        """
        set a live time to key
        :param key:
        :param ttl:
        :return:
        """
        pass

