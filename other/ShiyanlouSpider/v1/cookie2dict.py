# -*- coding: utf-8 -*-
# 2016/12/7
# author = JEFF


class MyCookie(object):
    def __init__(self):
        self.dict = {}
        with open('cookie_str.txt', 'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                list = line.split(':')
                self.dict[list[0]] = list[1][0:-1]

    def get_cook_dir(self):
        return self.dict


if __name__ == '__main__':
    print(MyCookie().get_cook_dir())
    print(type(MyCookie().get_cook_dir()))
