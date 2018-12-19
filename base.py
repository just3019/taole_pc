import threading
import time


# 控制台输出
def printf(s):
    print('[%s][%s]%s' % (threading.current_thread().getName(), time.strftime("%X"), s))


def write(file_path, s):
    f = open(file_path, "a")
    f.write('%s\n' % s.strip())
    f.close()
