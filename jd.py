import time

from base import printf, write
from web_driver import init_web_driver, close_web_driver


def jd_search_list(keyword):
    try:
        driver.get("https://search.jd.com/Search?keyword=%s" % keyword)
        products = driver.find_elements_by_class_name("gl-item")
        for p in products:
            id = p.get_attribute("data-sku")
            name = p.find_element_by_class_name("p-name").text
            price = p.find_element_by_tag_name("i").text
            url = p.find_element_by_class_name("p-name").find_element_by_tag_name("a").get_attribute("href")
            write("test.log", "%s|%s|%s|%s\n" % (id, name, price, url))
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
