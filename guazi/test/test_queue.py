# -*- coding: utf-8 -*-
# 2017/1/13

import queue
from multiprocessing import Queue, Process


def doset(q):
    for i in range(10000):
        q.put(i)


def doget(q):
    while True:
        try:
            x = q.get(True, timeout=5)
            print(x)
        except queue.Empty:
            break


if __name__ == '__main__':
    q1 = Queue()
    p1 = Process(target=doset, args=(q1,))
    p2 = Process(target=doget, args=(q1,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
