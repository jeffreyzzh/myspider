# -*- coding: utf-8 -*-
# 2017/1/19
import random
import time
import requests
import json

touse_list = []
unuse_list = []


def init_proxypool():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=60&country=国内')
    ip_ports = json.loads(r.text)
    for uip in ip_ports:
        ip_dict = {
            'http': 'http://{}:{}'.format(uip[0], uip[1]),
            'https': 'https://{}:{}'.format(uip[0], uip[1])
        }
        touse_list.append(ip_dict)


def get_one_proxy():
    return random.choice(touse_list)


def mark_unuse_ip(ip_dict):
    if ip_dict in touse_list:
        touse_list.remove(ip_dict)
        unuse_list.append(ip_dict)


def append_ip_ondb():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=30&country=国内')
    ip_ports = json.loads(r.text)
    for uip in ip_ports:
        ip_dict = {
            'http': 'http://{}:{}'.format(uip[0], uip[1]),
            'https': 'https://{}:{}'.format(uip[0], uip[1])
        }
        touse_list.append(ip_dict)


def delete_ip_ondb():
    if unuse_list:
        pass
    for unuew in unuse_list:
        unuse_ip = unuew['http'].replace('http://', '').split(':')[0]
        requests.get('http://127.0.0.1:8000/delete?ip={}'.format(unuse_ip))


def listen_proxypool():
    while True:
        if len(unuse_list) > 20:
            delete_ip_ondb()
        if len(touse_list) < 20:
            append_ip_ondb()
        time.sleep(60 * 3)


if __name__ == '__main__':
    print(unuse_list)
    print(touse_list)
    info = {
        'http': 'http://123.22.44.221:1234',
        'https': 'https://123.22.44.221:1234'
    }
    ip = info['http'].replace('http://', '').split(':')[0]
    print(ip)
