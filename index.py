import time

from base import printf
from kl import kl_search_list
from sn import sn_search_list
from thread_pool import ThreadPool


def index_deal(keyword, num):
    try:
        t = time.time()
        for i in range(0, num):
            kl_search_list(keyword)
            sn_search_list(keyword)
            time.sleep(10)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        printf(e)


if __name__ == '__main__':
    key = input("输入搜索的关键字：")
    count = eval(input("创建几个任务："))
    num = eval(input("一个任务循环多少次："))
    t = time.time()
    Tp = ThreadPool(1)
    for i in range(0, count):
        printf("执行第%s轮任务" % i)
        Tp.add_task(index_deal, key, num)
    Tp.wait_completion()
    printf(time.time() - t)
