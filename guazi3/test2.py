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
        xy = l.copy()
        for i in range(size):
            m = max(xy)
            m_index = xy.index(m)
            max_index.append(m_index)
            xy[m_index] = 0
            if i == size - 1:
                while True:
                    m2 = max(xy)
                    if m2 == m:
                        m2_index = xy.index(m2)
                        max_index.append(m2_index)
                        xy[m2_index] = 0
                    else:
                        break
        return max_index


if __name__ == '__main__':
    # print(find_max(lists, 3))
    # find_max(lists, 3)
    a = [4, 4, 1, 2, 3, 4, 5, 2, 5, 5, 4]
    x = [54, 3, 9, 5, 1, 21, 6, 1, 86, 37, 46, 27, 13, 10, 5, 6, 1, 64, 21, 14, 1, 4, 10, 11, 1, 10, 5, 1, 2, 102, 1,
         28, 67, 1, 7, 75, 4, 29, 5, 9, 7, 20, 6, 14, 105, 12, 12, 5, 51, 7, 4, 1, 5, 8, 6, 1, 13, 64, 3, 73, 5, 9, 23,
         3, 4, 1, 10, 106, 2, 25, 19, 38, 52, 12, 5, 1, 1, 8, 3, 3, 1, 2]
    print(find_max(a, 4))
