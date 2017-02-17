# -*- coding: utf-8 -*-
# 2017/2/17

import threading
from multiprocessing import Queue

lock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, workQueue, timeout=30, *kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        self.timeout = timeout
        self.setDaemon(True)
        self.workQueue = workQueue
        self.start()

    def run(self):
        while True:
            try:
                lock.acquire()
                callable, args = self.workQueue.get(time=self.timeout)
                res = callable(args)
                lock.release()
            except Queue.empty():
                break
            except Exception as e:
                print(e)
