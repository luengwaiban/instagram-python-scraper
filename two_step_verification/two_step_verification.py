# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
import cache
import exception


class TwoStepVerification(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_verification_type(self, possible_values):
        """
        get the verification type
        :param possible_values:
        :return:
        """
        pass

    @abstractmethod
    def get_security_code(self):
        """
        get the security code and use it to complete verification
        :return:
        """
        pass
