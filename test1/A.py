# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF


class A(object):
    def __init__(self):
        self.str1 = "helloworld"

    def get_str(self):
        return self.str1


if __name__ == '__main__':
    a = A()
    print(a.str1)
    print(a.get_str())
