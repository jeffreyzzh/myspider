# -*- coding: utf-8 -*-
# 2017/3/30


def get_headers(filepath='headers.txt'):
    with open(filepath, 'r') as f:
        cont = f.read()
    headers = cont.split('\n')
    headers_dict = {}
    for header in headers:
        s = header.split(':', 1)
        headers_dict[s[0]] = s[1]
    return headers_dict


if __name__ == '__main__':
    print(get_headers())
