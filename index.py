from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# 启动driver
def init_web_driver():
    global driver
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('window-size=800x600')
    driver_path = r'./chromedriver_mac'  # 这里放的就是下载的driver本地路径
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
    driver.implicitly_wait(10)


# 关掉driver
def close_web_driver():
    driver.quit()


if __name__ == '__main__':
    init_web_driver()
    try:
        driver.get("https://www.suning.com/")
        text = driver.find_element_by_id("searchKeywords")
        search = driver.find_element_by_id("searchSubmit")
        text.send_keys("iphonexsmax")
        search.click()
        driver.save_screenshot("screen.png")
        html = BeautifulSoup(driver.page_source, "lxml")
        products = html.select(".item-wrap")
        # products = driver.find_elements_by_xpath('//div[@class="item-bg"]')
        # print("products:%s" % products.count())
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

    close_web_driver()
