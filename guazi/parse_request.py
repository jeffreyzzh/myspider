# -*- coding: utf-8 -*-
# 2017/1/18 0018
# JEFF


import requests


def requesturl(url):
    resp = requests.get(url)
    _encode = resp.encoding
    return resp.content.decode(_encode)
