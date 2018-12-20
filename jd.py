import json
import time

from base import printf, write
from taole import feedbacks
from web_driver import init_web_driver, close_web_driver


def jd_search_list(keyword):
    try:
        driver.get("https://www.jd.com")
        key = driver.find_element_by_id("key")
        btn = driver.find_element_by_class_name("button")
        key.send_keys(keyword)
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
        # printf(params)
        p = json.dumps(params)
        feedbacks(p)
        write("jd-%s%s.log" % (keyword, time.strftime("%Y%m%d")), "%s\n" % params)
    except RuntimeError as e:
        printf("错误：%s" % e)


def jd_deal(keyword, num):
    global driver
    try:
        driver = init_web_driver()
        t = time.time()
        for i in range(0, num):
            jd_search_list(keyword)
            time.sleep(10)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    finally:
        close_web_driver(driver)


if __name__ == '__main__':
    key = input("输入搜索的关键字：")
    count = eval(input("创建几个任务："))
    num = eval(input("一个任务循环多少次："))
    t = time.time()
    for i in range(0, count):
        printf("开始第%s个任务" % i)
        jd_deal(key, num)
    printf(time.time() - t)
