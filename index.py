import time

import base
from jd import jd_deal
from schedule_task import tao_sche_thread
from thread_pool import ThreadPool

if __name__ == '__main__':
    Tp = ThreadPool(1)
    t = time.time()
    for i in range(0, 100):
        base.printf("创建%s个线程" % i)
        Tp.add_task(jd_deal, "西门子洗衣机 滚筒 10公斤", 100)
    Tp.wait_completion()
    base.printf(time.time() - t)
