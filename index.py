import threading
import time
from tkinter import *

from base import printf
from kl import kl_search_list
from sn import sn_search_list
from thread_pool import ThreadPool


def log(s):
    printf(s)
    textView.insert(END, '[%s][%s]%s\n' % (threading.current_thread().name, time.strftime("%X"), s))
    textView.update()
    textView.see(END)


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
            kl_search_list(key, low, high, taskId)
            sn_search_list(key, low, high, taskId)
            time.sleep(1)
        t1 = time.time()
        log("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        printf(e)


def ui():
    root = Tk()  # 创建窗口对象的背景色
    root.title('监控工具')
    root.geometry('320x210')

    fm1 = Frame(root)
    fm1.pack(fill=X)
    Label(fm1, text='任务id').pack(side=LEFT)
    global task
    task = Entry(fm1, width=4)
    task.pack(side=LEFT)
    Label(fm1, text='搜索内容').pack(side=LEFT)
    global entry
    entry = Entry(fm1, width=100)
    entry.pack(side=LEFT)

    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, height=10, yscrollcommand=s1.set)
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)

    fm2 = Frame(root)
    fm2.pack()
    Button(fm2, text='开始', command=submit).pack(side=LEFT)
    root.mainloop()


def submit():
    task_id = int(task.get())
    key = entry.get()
    t = threading.Thread(target=thread, args=(task_id, key,))
    t.setDaemon(True)
    t.start()


def thread(taskId, key):
    Tp = ThreadPool(1)
    i = 1
    while True:
        log("执行第%s轮任务" % i)
        Tp.add_task(index_deal, key, taskId)
        i += 1
        time.sleep(10)


if __name__ == '__main__':
    ui()
