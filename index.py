import time

from base import printf
from kl import kl_search_list
from sn import sn_search_list
from thread_pool import ThreadPool


def index_deal(keyword):
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
            kl_search_list(key, low, high)
            sn_search_list(key, low, high)
            time.sleep(1)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        printf(e)


if __name__ == '__main__':
    key = input("输入关键字(name,1000,2000|name2,2000,3000)：")
    Tp = ThreadPool(1)
    i = 1
    while True:
        printf("执行第%s轮任务" % i)
        Tp.add_task(index_deal, key)
        i += 1
        time.sleep(10)
