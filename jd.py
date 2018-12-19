import json
import time

from base import printf, write
from taole import feedbacks
from web_driver import init_web_driver, close_web_driver


def jd_search_list(keyword):
    try:
        driver.get("https://search.jd.com/Search?keyword=%s" % keyword)
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
            printf(dict)
            feedback_list.append(dict)
            write("test.log", "%s\n" % (dict))
        params = {"feedbacks": feedback_list}
        p = json.dumps(params)
        printf(p)
        feedbacks(p)
    except RuntimeError as e:
        printf("错误：%s" % e)


def jd_deal(keyword, num):
    global driver
    try:
        driver = init_web_driver()
        t = time.time()
        for i in range(0, num):
            jd_search_list(keyword)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    finally:
        close_web_driver(driver)


if __name__ == '__main__':
    jd_deal("iphonexsmax", 1)
