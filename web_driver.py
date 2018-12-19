# 启动driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init_web_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--hide-scrollbars')
    driver_path = r'./chromedriver_mac'  # 这里放的就是下载的driver本地路径
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
    driver.implicitly_wait(10)
    return driver


# 关掉driver
def close_web_driver(driver):
    driver.quit()
