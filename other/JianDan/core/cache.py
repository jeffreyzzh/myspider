# -*- coding: utf-8 -*-
# 2016/12/17 0017
# JEFF

from abc import ABCMeta, abstractmethod

CACHE_DIR = './.cache'


class CacheKeyNotExistError(IndexError):
    pass


class ICache:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass


class DiskCache(ICache):
    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = cache_dir

    def get(self, key):
        try:
            with open(key) as f:
                return f.read()
        except IOError:
            raise CacheKeyNotExistError

    def set(self, key, value):
        with open(key, 'w') as f:
            f.write(value)
