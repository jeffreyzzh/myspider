# -*- coding: utf-8 -*-
# 2016/12/15

'''

spider novel model

'''


class Novel(object):
    __slots__ = ('name', 'chapter_url_list', 'chapter_name_list')


class Chapter(object):
    __slots__ = ('chapter', 'content')

    # def __str__(self):
    #     print('chapter :{}'.format(self.chapter))
    #     print('content :{}'.format(self.content))


if __name__ == '__main__':
    n = Novel()
    n.name = "xxx"
    print(n.name)
