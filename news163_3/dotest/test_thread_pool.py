# -*- coding: utf-8 -*-
# 2017/2/17

import threading
import traceback
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
                print(traceback.format_exc())


class ThreadPool(object):
    def __init__(self, num_of_threads):
        self.workQueue = Queue()
        self.threads = []
        self.createThreadPool(num_of_threads)

    def createThreadPool(self, num_of_threads):
        for i in range(num_of_threads):
            thread = MyThread(self.workQueue)
            self.threads.append(thread)

    def wait_for_complete(self):
        while len(self.threads):
            thread = self.threads.pop()
        if thread.isAlive():
            thread.join()

    def add_job(self, callable, *args):
        self.workQueue.put((callable, args))


