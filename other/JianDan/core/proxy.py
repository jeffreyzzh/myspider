# -*- coding: utf-8 -*-
# 2016/12/15

import re
import socket
import random
import httplib2
from abc import ABCMeta, abstractmethod
from urllib.error import URLError, HTTPError


class Proxy(object):
    def __init__(self, protocol, ip, port):
        self.protocol = protocol
        self.ip = ip
        self.port = port

    def assemble(self):
        return '{}://{}:{}'.format(self.protocol, self.ip, self.port)


class IProxyFinder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self):
        '''returns a list of Proxy objects'''
        pass
