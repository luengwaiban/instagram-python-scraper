# -*- coding:utf-8 -*-

import os
import pickle
import time
import re
from cache.cache import Cache


class DiskCache(Cache):

    def __init__(self):
        self.cache_storage_dir = './cache_files'
        self.cache_storage_file_name = 'cache'
        if not os.path.exists(self.cache_storage_dir):
            os.makedirs(self.cache_storage_dir)
        file_path = self.get_cache_file_path()
        if not os.path.exists(file_path):
            open(file_path, mode='a').close()
            with open(file_path, mode='rb+') as f:
                pickle.dump({}, f)

    def get(self, key, default=None):
        cache_file = self.get_cache_file_path()
        cache_dict = self.read_cache(cache_file)
        if key not in cache_dict:
            return default
        if (cache_dict[key]['ttl']) and (cache_dict[key]['expire_at'] < time.time()):
            del cache_dict[key]
            self.write_cache(cache_file, cache_dict)
            return default
        return cache_dict[key]['value']

    def set(self, key, value, ttl=0):
        expire_at = 0
        if ttl:
            expire_at = time.time() + ttl
        cache_file = self.get_cache_file_path()
        cache_dict = self.read_cache(cache_file)
        dict_to_set = {'key': key, 'value': value, 'ttl': ttl, 'expire_at': expire_at}
        cache_dict[key] = dict_to_set
        self.write_cache(cache_file, cache_dict)

    def delete(self, key):
        cache_file = self.get_cache_file_path()
        cache_dict = self.read_cache(cache_file)
        if key not in cache_dict:
            return False
        del cache_dict[key]
        return True

    def keys(self, regex=''):
        cache_file = self.get_cache_file_path()
        cache_dict = self.read_cache(cache_file)

        def match_key(key):
            if (cache_dict[key]['ttl']) and (cache_dict[key]['expire_at'] < time.time()):
                del cache_dict[key]
                return re.search(regex, key) and True or False

        keys = list(cache_dict.keys())
        self.write_cache(cache_file, cache_dict)
        if not regex:
            return keys
        keys = filter(match_key, keys)
        return keys

    def ttl(self, key, ttl=0):
        cache_file = self.get_cache_file_path()
        cache_dict = self.read_cache(cache_file)
        if key not in cache_dict:
            return False
        cache_dict[key]['ttl'] = ttl
        cache_dict[key]['expire_at'] = cache_dict[key]['expire_at'] and cache_dict[key]['expire_at'] + ttl or time.time() + ttl
        self.write_cache(cache_file, cache_dict)
        return True

    def set_cache_storage_dir(self, directory='../cache_files'):
        self.cache_storage_dir = directory.rstrip('/')
        if not os.path.exists(self.cache_storage_dir):
            os.makedirs(self.cache_storage_dir)

    def set_cache_file_name(self, file_name='cache'):
        self.cache_storage_file_name = file_name
        file_path = self.get_cache_file_path()
        if not os.path.exists(file_path):
            open(file_path, mode='a').close()

    def get_cache_file_path(self):
        return self.cache_storage_dir+'/'+self.cache_storage_file_name

    def read_cache(self, filepath=''):
        try:
            with open(filepath, mode='rb+') as f:
                res = pickle.load(f)
                return res
        except EOFError:
            with open(filepath, mode='wb+') as f:
                pickle.dump({}, f)

    def write_cache(self, filepath='', data=None):
        data = data and data or {}
        with open(filepath, mode='wb+') as f:
            pickle.dump(data, f)
