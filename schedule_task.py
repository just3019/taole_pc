import os
import threading
import time

import schedule as schedule


def clean():
    os.system("kill -9 `ps -ef | grep headless | awk '{print$2}'`")
    os.system("kill -9 `ps -ef | grep chromedriver | awk '{print$2}'`")


def tao_sche():
    schedule.every(30).minutes.do(clean)
    while True:
        schedule.run_pending()
        time.sleep(1)


def tao_sche_thread():
    th = threading.Thread(target=tao_sche)
    th.setDaemon(True)
    th.start()
