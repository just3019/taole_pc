import threading
import time
from threading import Thread
from queue import Queue

import requests


class ThreadPool:
    def __init__(self, number_of_workers):
        self.tasks_queue = Queue(number_of_workers)
        self.result_queue = Queue(0)
        for _ in range(number_of_workers):
            ThreadWorker(self.tasks_queue, self.result_queue)

    def add_task(self, func, *args, **kwargs):
        self.tasks_queue.put((func, args, kwargs))

    def wait_completion(self):
        self.tasks_queue.join()
        _result = []
        while not self.result_queue.empty():
            _result.append(self.result_queue.get())
        return _result


class ThreadWorker(Thread):
    def __init__(self, tasks_queue, result_queue):
        Thread.__init__(self)
        self.tasks_queue = tasks_queue
        self.result_queue = result_queue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks_queue.get()
            try:
                r = func(*args, **kwargs)
                self.result_queue.put(r)
            except Exception as e:
                print(e)
                self.result_queue.put(e)
            finally:
                self.tasks_queue.task_done()


def lookup(word):
    print(f"查询{word}")
    r = requests.get(url='http://xtk.azurewebsites.net/BingDictService.aspx', params={'Word': word}, timeout=1)
    return r.json()


if __name__ == '__main__':
    TP = ThreadPool(5)
    for word in ['apple', 'banana', 'pear', 'grip', 'watermelon', 'raspberry', 'strawberry'] * 1:
        TP.add_task(lookup, word)
        time.sleep(1)
    time.sleep(5)
    #
    # result = TP.wait_completion()
    # for i in result:
    #     if isinstance(i, dict):
    #         print(i['defs'])


