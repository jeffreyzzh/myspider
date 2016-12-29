# -*- coding: utf-8 -*-
# 2016/12/29

import re
import socket
import random
import http.client
from abc import ABCMeta, abstractmethod
from urllib.error import HTTPError, URLError


class Proxy(object):
    def __init__(self, protocol, ip, port):
        self.protocol = protocol
        self.ip = ip
        self.port = port

    def assemble(self):
        return '{}://{}:{}'.format(self.protocol, self.ip, self.port)


class IProxyFinder(Proxy):
    __metaclass__ = ABCMeta

    @abstractmethod
    def finder(self):
        """
        :return a list of Proxy object
        """
        pass


class MiniProxyFinder(IProxyFinder):
    def __init__(self):
        pass
