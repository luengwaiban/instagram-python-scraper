# -*- coding:utf-8 -*-

from functools import reduce
import signal


def get_from_dict(data_dict, map_list, default=None):
    def getitem(source, key):
        try:
            if isinstance(source, list):
                return source[int(key)]
            if isinstance(source, dict) and key not in source.keys():
                return default
            if not source:
                return default
        except IndexError:
            return default

        return source[key]

    if isinstance(map_list, str):
        map_list = map_list.split('.')

    return reduce(getitem, map_list, data_dict)


def set_timeout(num, callback):
    """
    A decorator to limit the method run time.
    example:
    def after_timeout(): # callback function
        print("Time out!")
    @set_timeout(2, after_timeout) # 2s limited
    def connect():
        time.sleep(3)
        print('Finished without timeout.')

    :param num:
    :param callback:
    :return:
    """
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError as e:
                callback()
        return to_do
    return wrap
