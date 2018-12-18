import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def write(s):
    f = open("test.log", "a")
    f.write('%s\n' % s.strip())
    f.close()


# 启动driver
def init_web_driver():
    global driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    driver_path = r'./chromedriver_mac'  # 这里放的就是下载的driver本地路径
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
    driver.implicitly_wait(10)


# 关掉driver
def close_web_driver():
    driver.quit()


def sn_search_list(keyword):
    try:
        driver.get("https://search.suning.com/%s" % keyword)
        html = BeautifulSoup(driver.page_source, "lxml")
        products = html.select(".item-wrap")
        num = 0
        for product in products:
            id = product["id"]
            name = product.select(".title-selling-point")[0].text
            url = product.select(".img-block")[0].a["href"]

            # price = product.find_element_by_class_name("def-price").text
            # p = '%s|%s' % (name, price)
            num += 1
            print("%s\n" % product)
    except RuntimeError as e:
        print("错误：%s" % e)


def jd_search_list(keyword):
    try:
        init_web_driver()
        driver.get("https://search.jd.com/Search?keyword=%s" % keyword)
        products = driver.find_elements_by_class_name("gl-item")
        for p in products:
            id = p.get_attribute("data-sku")
            name = p.find_element_by_class_name("p-name").text
            price = p.find_element_by_tag_name("i").text
            url = p.find_element_by_class_name("p-name").find_element_by_tag_name("a").get_attribute("href")
            write("%s|%s|%s|%s\n" % (id, name, price, url))
    except RuntimeError as e:
        print("错误：%s" % e)
    finally:
        close_web_driver()


if __name__ == '__main__':
    t = time.time()
    for i in range(0, 5):
        t0 = time.time()
        jd_search_list("iphonexsmax")
        print("第%s次完成,耗时%s" % (i, time.time() - t0))
    t1 = time.time()
    print(t1 - t)
