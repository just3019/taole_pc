import threading
import time

from base import printf
from gm import gm_search_list
from jd_new import jd_new_search_list
from sn_new import sn_search_list
from thread_pool import ThreadPool
from ymx import ymx_search_list

searchTp = ThreadPool(1)


def index_deal(keyword, taskId=0):
    try:
        t = time.time()
        keylist = keyword.split("|")
        for keyk in keylist:
            keyr = keyk.split(",")
            key = keyr[0]
            low = keyr[1]
            high = keyr[2]
            if low == "":
                low = "0"
            if high == "":
                high = "99999"
            # searchTp.add_task(kl_search_list, key, low, high, taskId)
            searchTp.add_task(sn_search_list, key, low, high, taskId)
            searchTp.add_task(gm_search_list, key, low, high, taskId)
            searchTp.add_task(ymx_search_list, key, low, high, taskId)
            searchTp.add_task(jd_new_search_list, key, low, high, taskId)
            # time.sleep(1)
        searchTp.wait_completion()
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        printf(e)


def submit(taskId, key):
    task_id = taskId
    if task_id is None:
        task_id = 0
    key = key
    t = threading.Thread(target=thread, args=(task_id, key,))
    t.setDaemon(True)
    t.start()


def thread(taskId, key):
    Tp = ThreadPool(1)
    i = 1
    while True:
        printf("执行第%s轮任务" % i)
        Tp.add_task(index_deal, key, taskId)
        i += 1
        time.sleep(5)


if __name__ == '__main__':
    submit()
    while True:
        time.sleep(1000)
