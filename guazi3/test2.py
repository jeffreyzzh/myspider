# -*- coding: utf-8 -*-
# 2017/1/26 0026
# JEFF

lists = [1, 2, 3, 4, 5, 5, 2, 5]


# x = lists.copy()
# print(x)
#
# a = max(x)
# print('max:', a)
# x.pop(a)
# print('lisr len:', len(x))
# print('max index:', x.index(a))


def find_max(l, size):
    max_index = []
    if not l or not isinstance(size, int):
        return max_index
    if len(l) <= size:
        return [each for each in range(len(l))]
    else:
        x = l.copy()
        for i in range(size):
            m = max(x)
            max_index.append(x.index(m) + i)
            x.remove(m)
        return max_index


if __name__ == '__main__':
    # print(find_max(lists, 3))
    # find_max(lists, 3)
    print(find_max(lists, 4))
