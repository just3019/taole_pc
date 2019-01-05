import json
import threading
import time
from tkinter import *

from base import printf, write
from taole import feedbacks
from thread_pool import ThreadPool
from web_driver import init_web_driver, close_web_driver


def log(s):
    printf(s)
    textView.insert(END, '[%s][%s]%s\n' % (threading.current_thread().name, time.strftime("%X"), s))
    textView.update()
    textView.see(END)


def jd_search_list(keyword):
    keylist = keyword.split(",")
    for k in keylist:
        try:
            driver.get("https://www.jd.com")
            key = driver.find_element_by_id("key")
            btn = driver.find_element_by_class_name("button")
            key.send_keys(k)
            btn.click()
            products = driver.find_elements_by_class_name("gl-item")
            feedback_list = []
            for p in products:
                id = p.get_attribute("data-sku")
                name = p.find_element_by_class_name("p-name").text
                price = p.find_element_by_tag_name("i").text
                url = p.find_element_by_class_name("p-name").find_element_by_tag_name("a").get_attribute("href")
                price_dict_list = []
                price_dict = {"price": price}
                price_dict_list.append(price_dict)
                dict = {"url": url, "lowPrice": price, "price": price, "name": name, "productId": id,
                        "feedbackPrices": price_dict_list}
                # printf(dict)
                feedback_list.append(dict)
            params = {"feedbacks": feedback_list}
            p = json.dumps(params)
            # printf(p)
            feedbacks(p)
            write("jd-%s%s.log" % (k, time.strftime("%Y%m%d")), "%s\n" % params)
        except RuntimeError as e:
            printf("错误：%s" % e)


def jd_deal(keyword, num):
    global driver
    t = time.time()
    try:
        driver = init_web_driver()
        for i in range(0, num):
            jd_search_list(keyword)
            time.sleep(10)
    finally:
        close_web_driver(driver)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))


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
    key = entry.get()
    t = threading.Thread(target=thread, args=(key,))
    t.setDaemon(True)
    t.start()


def thread(key):
    Tp = ThreadPool(1)
    i = 1
    while True:
        log("执行第%s轮任务" % i)
        Tp.add_task(jd_deal, key, 100)
        i += 1
        time.sleep(5)


if __name__ == '__main__':
    ui()
