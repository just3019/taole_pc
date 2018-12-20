import time

import base
from jd import jd_deal

if __name__ == '__main__':
    t = time.time()
    for i in range(0, 100):
        base.printf("创建%s个线程" % i)
        jd_deal("西门子洗衣机 滚筒 10公斤", 100)
    base.printf(time.time() - t)
