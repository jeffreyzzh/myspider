# -*- coding: utf-8 -*-
# 2017/1/19

def pritty_exception_info(e):
    if not e:
        return 'no exception info'
    string = '>> - ' * 30 + '\r\n'
    string += str(e) + '\r\n'
    string += '<< - ' * 30 + '\r\n'
    return string


if __name__ == '__main__':
    print(pritty_exception_info('exception!!!!!!!!!!!!!!'))
