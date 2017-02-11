# -*- coding: utf-8 -*-
# 2017/2/11 0011
# JEFF

from test1.A import A


class B(A):
    def __init__(self):
        super().__init__()
        self.str2 = 'hellopython'
        # A.__init__(self)

    def getstr1(self):
        return self.str1


if __name__ == '__main__':
    b = B()
    print(b.str1)
    print(b.str2)
